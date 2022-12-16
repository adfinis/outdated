"""Generalized access to enviromental variables."""
import environ

env = environ.Env()
env.read_env(".env")
