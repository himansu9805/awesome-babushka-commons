"""RabbitMQ client configuration."""

import logging
from typing import Optional, Dict, Any

import aio_pika
from aio_pika import ExchangeType

from commons.models import SingletonMeta

logger = logging.getLogger(__name__)


class RabbitMQClient(metaclass=SingletonMeta):
    """RabbitMQ client for managing connections and topology."""

    def __init__(
        self,
        connection_url: str,
        reconnect_interval: int = 5,
        prefetch_count: int = 10,
    ):
        """
        Initialize RabbitMQ client.

        Args:
            connection_url: RabbitMQ connection URL.
            reconnect_interval: Seconds to wait before reconnecting.
            prefetch_count: Max unacknowledged messages per consumer.
        """
        self._connection: Optional[aio_pika.RobustConnection] = None
        self._channel: Optional[aio_pika.Channel] = None
        self._reconnect_interval = reconnect_interval
        self._prefetch_count = prefetch_count
        self._connection_url = connection_url

    async def connect(self) -> None:
        """
        Opens a robust connection and a single shared channel.
        RobustConnection automatically reconnects on dropped connections.
        """
        self._connection = await aio_pika.connect_robust(
            self._connection_url, reconnect_interval=self._reconnect_interval
        )  # type: ignore
        self._channel = await self._connection.channel()  # type: ignore

        # Limit unacknowledged messages per consumer — prevents a slow
        # consumer from being overwhelmed if the queue backs up
        await self._channel.set_qos(prefetch_count=self._prefetch_count)  # type: ignore

        logger.info("RabbitMQ connection established")

    async def close(self) -> None:
        """Closes the existing open connection."""
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
            logger.info("RabbitMQ connection closed")

    def get_channel(self) -> aio_pika.Channel:
        """Get channel for publishing messages to an exchange."""
        if self._channel is None:
            raise RuntimeError(
                "RabbitMQ is not connected. Call connect() first."
            )
        return self._channel

    async def declare_exchange(
        self,
        exchange_name: str,
        exchange_type: ExchangeType = ExchangeType.FANOUT,
        durable: bool = True,
    ) -> aio_pika.Exchange:
        """
        Declare an exchange.

        Args:
            exchange_name: Name of the exchange.
            exchange_type: Type of exchange (FANOUT, DIRECT, TOPIC).
            durable: Whether exchange persists after broker restart.

        Returns:
            Declared exchange object.
        """
        channel = self.get_channel()
        return await channel.declare_exchange(
            exchange_name, exchange_type, durable=durable
        )  # type: ignore

    async def declare_queue(
        self,
        queue_name: str,
        durable: bool = True,
        arguments: Optional[Dict[str, Any]] = None,
    ) -> aio_pika.Queue:
        """
        Declare a queue.

        Args:
            queue_name: Name of the queue.
            durable: Whether queue persists after broker restart.
            arguments: Queue arguments (e.g., dead-letter config, TTL).

        Returns:
            Declared queue object.
        """
        channel = self.get_channel()
        return await channel.declare_queue(
            queue_name, durable=durable, arguments=arguments
        )  # type: ignore

    @staticmethod
    def queue_args_with_dlq(
        dead_letter_exchange: str,
        dead_letter_routing_key: str,
        ttl_ms: int = 86_400_000,
    ) -> Dict[str, Any]:
        """
        Generate queue arguments with dead-letter configuration.

        Args:
            dead_letter_exchange: Dead-letter exchange name.
            dead_letter_routing_key: Dead-letter routing key.
            ttl_ms: Message time-to-live in milliseconds (default: 24 hours).

        Returns:
            Dictionary of queue arguments.
        """
        return {
            "x-dead-letter-exchange": dead_letter_exchange,
            "x-dead-letter-routing-key": dead_letter_routing_key,
            "x-message-ttl": ttl_ms,
        }
