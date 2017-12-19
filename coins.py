from sys import argv
from copy import deepcopy

MAX_SIZE = 10
TRANS_COEF = 1000
START_MONEY = 1000000

def print_result(result, output_file):
    """Print result(list of tuples(country_name, country_params)) to output_file."""
    output_file.write("Case Number " + str(case) + '\n')
    for country_name, country_params in result:
        output_file.write(country_name + " " + str(country_params['result_day']) + '\n')

def sort_key(country):
    """Calculate unified key for country."""
    return country[1]['result_day'] * 26 + (ord(country[0][0]) - ord('A'))

def sort_countries(countries):
    """Sort dictionary of countries by unified key and make result list of tuples(country_name, country_params)."""
    return sorted(countries.items(), key=sort_key)

def checkEnding(country_map, countries, day):
    """Check if each country is completed, return True if all countries are completed, False otherwise."""
    for (i, line) in enumerate(country_map):
        for (j, elem) in enumerate(line):
            if (None != elem):
                if (0 == elem['money'].count(0)) and ((i, j) not in countries[elem['country_name']]['completed_towns']):
                    countries[elem['country_name']]['completed_towns'].append((i, j))
                    if (-1 == countries[elem['country_name']]['result_day']) and (len(countries[elem['country_name']]['completed_towns']) == countries[elem['country_name']]['towns_count']):
                        countries[elem['country_name']]['result_day'] = day
                elif (0 != elem['money'].count(0)) and ((i, j) in countries[elem['country_name']]['completed_towns']):
                    countries[elem['country_name']]['completed_towns'].remove((i, j))

    for country in countries.values():
        if -1 == country['result_day']:
            return False
    return True

def coinsTransfers(country_map):
    """Getting begin-day map country_map, make coins transactions, fill new matrix and return it."""
    matrix = deepcopy(country_map)
    for (i, line) in enumerate(country_map):
        for (j, elem) in enumerate(line):
            if None != elem:
                if (0 < i and None != matrix[i - 1][j]):
                    matrix[i][j]['money'] = map(lambda x, y: x - (y / TRANS_COEF), matrix[i][j]['money'], elem['money'])
                    matrix[i - 1][j]['money'] = map(lambda x, y: x + (y / TRANS_COEF), matrix[i - 1][j]['money'], elem['money'])
                if (0 < j and None != matrix[i][j - 1]):
                    matrix[i][j]['money'] = map(lambda x, y: x - (y / TRANS_COEF), matrix[i][j]['money'], elem['money'])
                    matrix[i][j - 1]['money'] = map(lambda x, y: x + (y / TRANS_COEF), matrix[i][j - 1]['money'], elem['money'])
                if (i < (MAX_SIZE - 1) and None != matrix[i + 1][j]):
                    matrix[i][j]['money'] = map(lambda x, y: x - (y / TRANS_COEF), matrix[i][j]['money'], elem['money'])
                    matrix[i + 1][j]['money'] = map(lambda x, y: x + (y / TRANS_COEF), matrix[i + 1][j]['money'], elem['money'])
                if (j < (MAX_SIZE - 1) and None != matrix[i][j + 1]):
                    matrix[i][j]['money'] = map(lambda x, y: x - (y / TRANS_COEF), matrix[i][j]['money'], elem['money'])
                    matrix[i][j + 1]['money'] = map(lambda x, y: x + (y / TRANS_COEF), matrix[i][j + 1]['money'], elem['money'])
    return matrix

def coinsProcess(country_map, countries):
    """Main task cycle. Return resulting dictionary of countries when checkEnding is True, execute coinsTransfers otherwise."""
    day = 0
    while True:
        if checkEnding(country_map, countries, day):
            return countries
        country_map = coinsTransfers(country_map)
        day += 1

def makeMatrix(input_file, count):
    """Reading input data of count countries from input_file, fill first-day matrix, dictionary of coutries and return them."""
    matrix = [[None for i in xrange(MAX_SIZE)] for i in xrange(MAX_SIZE)]
    countries = {}
    for cnt in xrange(count):
        country = input_file.readline().split(' ')
        country_name = (country[0])
        (xlt, ylt, xrb, yrb) = map(lambda x: int(x) - 1, country[1:])
        for i in xrange(ylt, yrb + 1):
            for j in xrange(xlt, xrb + 1):
                matrix[i][j] = dict()
                matrix[i][j]['country_name'] = country_name
                matrix[i][j]['country_code'] = cnt
                matrix[i][j]['money'] = [0] * count
                matrix[i][j]['money'][cnt] = START_MONEY
        countries[country_name] = dict()
        countries[country_name]['completed_towns'] = []
        countries[country_name]['towns_count'] = (yrb - ylt + 1) * (xrb - xlt + 1)
        countries[country_name]['result_day'] = -1
    return (matrix, countries)

if __name__ == "__main__":
    input_file  = "input.txt" if 1 == len(argv) else argv[1]
    output_file = "output.txt"
    ifile = open(input_file)
    ofile = open(output_file, "w")
    count = int(ifile.readline())
    case = 1
    while 0 < count:
        (country_map, countries) = makeMatrix(ifile, count)
        countries = coinsProcess(country_map, countries)
        result = sort_countries(countries)
        print_result(result, ofile)
        count = int(ifile.readline())
        case += 1
    ifile.close()
    ofile.close()
        
