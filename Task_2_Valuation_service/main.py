import csv


def load_currencies(file_path):
    """
    Load currency data from the currencies.csv file.

    Args:
        file_path (str): Path to the currencies.csv file.

    Returns:
        dict: A dictionary containing currency code as keys and their corresponding ratios as values.
    """
    currencies = {}
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            currency = row['currency']
            ratio = float(row['ratio'])
            currencies[currency] = ratio
    return currencies


def load_data(file_path):
    """
    Load product data from the data.csv file.

    Args:
        file_path (str): Path to the data.csv file.

    Returns:
        list: A list of dictionaries containing product information.
    """
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            product = {
                'id': int(row['id']),
                'price': float(row['price']),
                'currency': row['currency'],
                'quantity': int(row['quantity']),
                'matching_id': int(row['matching_id'])
            }
            data.append(product)
    return data


def load_matchings(file_path):
    """
    Load matching data from the matchings.csv file.

    Args:
        file_path (str): Path to the matchings.csv file.

    Returns:
        list: A list of dictionaries containing matching information.
    """
    matchings = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            matching = {
                'matching_id': int(row['matching_id']),
                'top_priced_count': int(row['top_priced_count'])
            }
            matchings.append(matching)
    return matchings


def save_results(file_path, results):
    """
    Save the valuation results to a CSV file.

    Args:
        file_path (str): Path to the output CSV file.
        results (list): List of dictionaries containing the valuation results.

    Returns:
        None
    """
    fieldnames = ['matching_id', 'total_price', 'avg_price', 'currency', 'ignored_products_count']
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def calculate_valuation(data, matchings, currencies):
    """
    Calculate the valuation results based on the input data and matchings.

    Args:
        data (list): List of dictionaries containing product information.
        matchings (list): List of dictionaries containing matching information.
        currencies (dict): Dictionary containing currency codes and their ratios.

    Returns:
        list: List of dictionaries containing the valuation results.
    """
    valuation_results = []
    for matching in matchings:
        matching_id = matching['matching_id']
        top_priced_count = matching['top_priced_count']

        products = [product for product in data if product['matching_id'] == matching_id]
        products.sort(key=lambda x: x['price'] * x['quantity'], reverse=True)
        top_products = products[:top_priced_count]
        ignored_products_count = len(products) - top_priced_count

        total_price = sum(product['price'] * product['quantity'] for product in top_products)
        avg_price = total_price / top_priced_count

        currency = top_products[0]['currency']
        if currency != 'PLN':
            ratio = currencies[currency]
            total_price *= ratio
            avg_price *= ratio
            currency = 'PLN'

        result = {
            'matching_id': matching_id,
            'total_price': total_price,
            'avg_price': avg_price,
            'currency': currency,
            'ignored_products_count': ignored_products_count
        }
        valuation_results.append(result)

    return valuation_results


# Unit test for loading currencies
def test_load_currencies():
    currencies = load_currencies('currencies.csv')
    assert len(currencies) == 3
    assert currencies['GBP'] == 2.4
    assert currencies['EU'] == 2.1
    assert currencies['PLN'] == 1.0


# Unit test for loading data
def test_load_data():
    data = load_data('data.csv')
    assert len(data) == 9
    assert data[0]['id'] == 1
    assert data[0]['price'] == 1000.0
    assert data[0]['currency'] == 'GBP'
    assert data[0]['quantity'] == 2
    assert data[0]['matching_id'] == 3


# Unit test for loading matchings
def test_load_matchings():
    matchings = load_matchings('matchings.csv')
    assert len(matchings) == 3
    assert matchings[0]['matching_id'] == 1
    assert matchings[0]['top_priced_count'] == 2


# Unit test for saving results
def test_save_results():
    results = [
        {'matching_id': 1, 'total_price': 6200.0, 'avg_price': 3100.0, 'currency': 'GBP', 'ignored_products_count': 1},
        {'matching_id': 2, 'total_price': 24500.0, 'avg_price': 12250.0, 'currency': 'PLN', 'ignored_products_count': 0},
        {'matching_id': 3, 'total_price': 12750.0, 'avg_price': 4250.0, 'currency': 'EU', 'ignored_products_count': 1}
    ]
    save_results('top_products.csv', results)


# Function to run all unit tests
def run_unit_tests():
    test_load_currencies()
    test_load_data()
    test_load_matchings()
    test_save_results()


def create_input_files():
    # Create currencies.csv file
    currencies_data = [
        {'currency': 'GBP', 'ratio': '2.4'},
        {'currency': 'EU', 'ratio': '2.1'},
        {'currency': 'PLN', 'ratio': '1.0'}
    ]
    with open('currencies.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['currency', 'ratio'])
        writer.writeheader()
        writer.writerows(currencies_data)

    # Create data.csv file
    data = [
        {'id': '1', 'price': '1000', 'currency': 'GBP', 'quantity': '2', 'matching_id': '3'},
        {'id': '2', 'price': '1050', 'currency': 'EU', 'quantity': '1', 'matching_id': '1'},
        {'id': '3', 'price': '2000', 'currency': 'PLN', 'quantity': '1', 'matching_id': '1'},
        {'id': '4', 'price': '1750', 'currency': 'EU', 'quantity': '2', 'matching_id': '2'},
        {'id': '5', 'price': '1400', 'currency': 'EU', 'quantity': '4', 'matching_id': '3'},
        {'id': '6', 'price': '7000', 'currency': 'PLN', 'quantity': '3', 'matching_id': '2'},
        {'id': '7', 'price': '630', 'currency': 'GBP', 'quantity': '5', 'matching_id': '3'},
        {'id': '8', 'price': '4000', 'currency': 'EU', 'quantity': '1', 'matching_id': '3'},
        {'id': '9', 'price': '1400', 'currency': 'GBP', 'quantity': '3', 'matching_id': '1'}
    ]
    with open('data.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'price', 'currency', 'quantity', 'matching_id'])
        writer.writeheader()
        writer.writerows(data)

    # Create matchings.csv file
    matchings = [
        {'matching_id': '1', 'top_priced_count': '2'},
        {'matching_id': '2', 'top_priced_count': '2'},
        {'matching_id': '3', 'top_priced_count': '3'}
    ]
    with open('matchings.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['matching_id', 'top_priced_count'])
        writer.writeheader()
        writer.writerows(matchings)


if __name__ == '__main__':
    # Create input files
    create_input_files()

    # Load input data
    currencies = load_currencies('currencies.csv')
    data = load_data('data.csv')
    matchings = load_matchings('matchings.csv')

    # Calculate valuation results
    results = calculate_valuation(data, matchings, currencies)

    # Save results to a file
    save_results('top_products.csv', results)

    # Run unit tests
    run_unit_tests()
