# Singleton

- Probably One of the most hated Design Patterns.
- "When discussing which patterns to drop, we found that we still love them all.(Not really-I'm in favor of dropping Singleton. Its use is almost always a design smell.)" - Erich Gamma
- For some components it only makes sense to have one in the system. e.g. Database repository, Object Factory
- Sometimes the initializer call is expensive. We only do it once. We provide everyone with the same instance.
- Want to prevent anyone creating additional copies.
- Need to take care of lazy instantiation.
- A Component which is instantiated only once.
