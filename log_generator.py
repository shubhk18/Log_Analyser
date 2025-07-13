import logging
import time
import random
import os

# Configure logging
log_file = "mysql_connection_detailed.log"
if os.path.exists(log_file):
    os.remove(log_file)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [ProcessID:%(process)d] - [ThreadID:%(thread)d] - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
    ]
)

queries = [
    "SELECT * FROM users WHERE age > %d",
    "INSERT INTO orders (user_id, product_id, quantity) VALUES (%d, %d, %d)",
    "UPDATE products SET price = %.2f WHERE id = %d",
    "DELETE FROM sessions WHERE user_id = %d",
    "SELECT COUNT(*) FROM logs WHERE timestamp > NOW() - INTERVAL '1 hour'"
]

users = ["admin", "john.doe", "jane.smith", "api_user", "guest"]

def simulate_detailed_mysql_connection(iteration):
    """Simulates a detailed C++ process connecting to a MySQL database."""
    user = random.choice(users)
    logging.info(f"Initiating connection for user '{user}' from host '192.168.1.{random.randint(2, 254)}'.")

    if random.random() < 0.05:
        logging.error("Failed to connect to MySQL database at 'localhost:3306': Connection timeout.")
        return

    logging.info("Connection successful. Authenticating user.")
    logging.info(f"User '{user}' authenticated successfully.")
    logging.debug("Connection added to pool. Pool size: %d", random.randint(5, 20))

    for _ in range(random.randint(1, 10)):
        query = random.choice(queries)
        start_time = time.time()
        if "SELECT" in query and "users" in query:
            params = (random.randint(18, 65),)
            logging.info(f"Executing query: {query % params}")
            time.sleep(random.uniform(0.01, 0.2))
            rows_returned = random.randint(0, 1000)
            logging.info(f"Query executed successfully. {rows_returned} rows returned.")
        elif "INSERT" in query:
            params = (random.randint(1, 1000), random.randint(1, 100), random.randint(1, 5))
            logging.info(f"Executing query: {query % params}")
            time.sleep(random.uniform(0.05, 0.3))
            logging.info("Query executed successfully. 1 row affected.")
        elif "UPDATE" in query:
            params = (random.uniform(10.0, 500.0), random.randint(1, 100))
            logging.info(f"Executing query: {query % params}")
            time.sleep(random.uniform(0.1, 0.5))
            if random.random() < 0.1:
                logging.warning("Query execution took longer than expected.")
            logging.info("Query executed successfully. 1 row updated.")
        elif "DELETE" in query:
            params = (random.randint(1, 1000),)
            logging.info(f"Executing query: {query % params}")
            time.sleep(random.uniform(0.02, 0.15))
            logging.info("Query executed successfully. 1 row deleted.")
        elif "COUNT" in query:
            logging.info(f"Executing query: {query}")
            time.sleep(random.uniform(0.01, 0.1))
            logging.info("Query executed successfully.")
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000
        logging.debug(f"Query execution time: {execution_time:.2f} ms.")


    logging.info(f"Closing connection for user '{user}'.")
    logging.debug("Connection removed from pool.")

if __name__ == "__main__":
    # Estimate: ~15 lines per iteration, ~150 bytes/line -> ~2.25 KB/iteration
    # For 50MB -> 50 * 1024 KB / 2.25 KB/iteration ~= 22755 iterations
    # Let's use 25000 to be safe
    total_iterations = 25000
    print(f"Generating detailed logs... This may take a few moments.")
    for i in range(total_iterations):
        simulate_detailed_mysql_connection(i)
        if (i + 1) % 1000 == 0:
            print(f"Progress: {i + 1}/{total_iterations} iterations completed.")
    print("Log generation complete.")
    file_size = os.path.getsize(log_file) / (1024 * 1024)
    print(f"Generated log file '{log_file}' with size: {file_size:.2f} MB")