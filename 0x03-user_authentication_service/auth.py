#!/usr/bin/env python3
"""Authentication module
"""
import bcrypt


def _hash_password(password: str) -> str:
    """Hash password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
