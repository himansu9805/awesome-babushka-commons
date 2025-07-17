# Awesome Babushka Commons

A shared Python package containing common utilities, models, and database connections for the Awesome Babushka ecosystem. This package provides reusable components that can be shared across multiple services in the Awesome Babushka platform.

## Features

- � **Common Models**: Shared data models and utilities like SingletonMeta
- �️ **Database Connections**: MongoDB connection utilities with singleton pattern
- � **Reusable Components**: Common functionality that can be shared across services
- 📦 **Easy Installation**: Installable as a pip package directly from GitHub

## Installation

You can install this package directly from GitHub:

```bash
pip install git+https://github.com/himansu9805/awesome-babushka-commons.git@main
```

Or add it to your `requirements.txt`:

```txt
git+https://github.com/himansu9805/awesome-babushka-commons.git@main
```

## Usage

### MongoDB Connection

```python
from commons import MongoConnect

# Create a MongoDB connection (singleton)
mongo = MongoConnect("mongodb://localhost:27017", "my_database")

# Get a collection
users_collection = mongo.get_collection("users")

# Use the collection
users_collection.insert_one({"name": "John", "email": "john@example.com"})

# Close connection when done
mongo.close()
```

### Singleton Pattern

```python
from commons import SingletonMeta

class MyService(metaclass=SingletonMeta):
    def __init__(self):
        self.initialized = True

# Both instances will be the same object
service1 = MyService()
service2 = MyService()
assert service1 is service2  # True
```

## Contributing

We welcome contributions from the community! Please open issues or submit pull requests for new features, bug fixes, or suggestions.

1. Fork the repository and create your feature branch.
2. Make your changes and add tests where appropriate.
3. Run linting and formatting checks.
4. Submit a pull request for review.

## License

[MIT](LICENSE) © 2025 Awesome Babushka Contributors

## Authors & Acknowledgments

- [@himansu9805](https://github.com/himansu9805)
- Special thanks to all contributors and the open-source community.

## Project Status

🚧 **Pre-alpha**: This project is under active development. Features and APIs are subject to change. Feedback and contributions are highly encouraged!
