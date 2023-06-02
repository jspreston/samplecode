from config_examples import ExHydraConfig


def test_instantiation():
    config_hierarchy = {
        "config.yaml": """
            defaults:
            - db: mysql
            """,
        "db": {
            "mysql.yaml": """
                _target_: my_app.MySQLConnection
                host: localhost
                user: root
                password: 1234
                """,
            "postgresql.yaml": """
                _target_: my_app.PostgreSQLConnection
                host: localhost
                user: root
                password: 1234
                database: tutorial
                """,
        },
    }
    ex = ExHydraConfig(config_hierarchy=config_hierarchy)

    md = ex.to_markdown()
    print(md)


if __name__ == "__main__":
    test_instantiation()
