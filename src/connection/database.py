from __future__ import annotations

import os

from dotenv import load_dotenv
import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import connection as Connection
from psycopg2.extras import execute_values


load_dotenv()


def get_connection() -> Connection:
	"""Open a PostgreSQL connection using the POSTGRES_* environment variables."""
	required_variables = (
		"POSTGRES_USER",
		"POSTGRES_PASSWORD",
		"POSTGRES_HOST",
		"POSTGRES_PORT",
		"POSTGRES_DB",
	)
	missing_variables = [name for name in required_variables if not os.getenv(name)]
	if missing_variables:
		raise RuntimeError(
			"Missing PostgreSQL environment variables: " + ", ".join(missing_variables)
		)

	return psycopg2.connect(
		dbname=os.environ["POSTGRES_DB"],
		user=os.environ["POSTGRES_USER"],
		password=os.environ["POSTGRES_PASSWORD"],
		host=os.environ["POSTGRES_HOST"],
		port=os.environ["POSTGRES_PORT"],
		sslmode="require",
		connect_timeout=30,
	)


def insert_df(df: pd.DataFrame, tablename: str) -> int:
	"""Insert a Pandas DataFrame into a PostgreSQL table.

	Returns the number of rows inserted.
	"""
	if df.empty:
		return 0

	if not tablename:
		raise ValueError("tablename cannot be empty")

	# Convert NaN/NaT to None so PostgreSQL receives NULL.
	df = df.astype(object).where(pd.notna(df), None)

	columns = list(df.columns)
	values = [tuple(row) for row in df.itertuples(index=False, name=None)]

	connection = get_connection()

	try:
		with connection.cursor() as cursor:
			query = sql.SQL("INSERT INTO {} ({}) VALUES %s").format(
				sql.Identifier(tablename),
				sql.SQL(", ").join(
					sql.Identifier(column) for column in columns
				),
			)

			execute_values(
				cursor,
				query.as_string(connection),
				values,
			)

		connection.commit()
		return len(values)

	except Exception:
		connection.rollback()
		raise

	finally:
		connection.close()
