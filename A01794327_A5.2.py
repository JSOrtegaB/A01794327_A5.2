"""
The Python script calculates the total sales cost from JSON data on product
prices and sales records, writing the results and execution time to both the
console and a file named SalesResults.txt, requieres 2 input files: The first
file will contain information in a JSON format about a catalogue of prices of
products. The second file will contain a record for all sales in a company"""

import json
import sys
import time


def load_json_file(filename):
    """Load JSON data from a file, handling specific exceptions."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON format in file: {filename}")
        return None
    except IOError as e:
        print(f"Unexpected error loading file {filename}: {e}")
        return None


def calculate_total_sales_cost(products, sales):
    """Calculate the total sales cost """
    prices = {product['title']: product['price'] for product in products}
    calculated_total_cost = 0
    for sale in sales:
        product_title = sale.get('Product')
        quantity = sale.get('Quantity', 0)
        if product_title in prices:
            calculated_total_cost += prices[product_title] * quantity
        else:
            print(
                    f"Warning: Product '{product_title}' "
                    f"not found in price catalogue."
            )
    return calculated_total_cost


def write_results_to_file(content):
    """Write results to a specified file, specifying encoding."""
    filename = "SalesResults.txt"
    try:
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(content)
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")


if __name__ == "__main__":
    start_time = time.time()

    if len(sys.argv) != 3:
        print("Usage: python computeSales.py"
              "priceCatalogue.json salesRecord.json")
        sys.exit(1)

    price_catalogue_filename = sys.argv[1]
    sales_record_filename = sys.argv[2]

    product_list = load_json_file(price_catalogue_filename)
    sales_list = load_json_file(sales_record_filename)

    if product_list is None or sales_list is None:
        sys.exit("Error: One or more files could not be loaded.")

    total_sales_cost = calculate_total_sales_cost(product_list, sales_list)

    results_content = (
        f"\nCatalogo: {price_catalogue_filename}\n"
        f"Lista: {sales_record_filename}\n"
        f"Total Sales Cost: ${total_sales_cost:.2f}\n"
    )
    execution_time = time.time() - start_time
    results_content += f"Execution Time: {execution_time:.4f} seconds\n"

    print(results_content)
    write_results_to_file(results_content)
