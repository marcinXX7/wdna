from typing import Tuple


class Dataset:

    def __init__(self, labels: list[str], data: list[list[str]]):
        self.__labels = labels
        self.__data = data

    def get_labels(self) -> list[str]:
        """
        :return: zwraca listę etykiet
        """
        if self.__labels is None or len(self.__labels) == 0:
            print('Brak etykiet w podanym datasecie')
        return self.__labels

    def get_data(self, start: int = None, end: int = None) -> list[list[str]]:
        """
        :param start: indeks od którego ma być stworzony podzbiór, domyślnie brak
        :param end: indeks do którego ma być stworzony podzbiór, domyślnie brak
        :return: zwraca zbiór lub podzibiór danych
        """

        return self.__data[start:end]

    def test_train_val_split(self, test_percentage: float, train_percentage: float, val_percentage: float) -> Tuple:
        """
        :param test_percentage: procentowa ilość rekordów z danych, które trafią do zbioru treningowego
        :param train_percentage: procentowa ilość rekordów z danych, które trafią do zbioru testowego
        :param val_percentage: procentowa ilość rekordów z danych, które trafią do zbioru walidacyjnego
        :return: krotka 3-elementowa z poszczególnymi podzbiorami
        """

        if test_percentage + train_percentage + val_percentage != 1:
            print('Suma procentów musi się równać 1.0')
            return None, None, None

        data_length = len(self.__data)
        if data_length < 3:
            print('Danych nie da się podzielić na 3 części')
            return None, None, None

        cumulative_sum_percentages = [test_percentage,
                                      test_percentage + train_percentage,
                                      test_percentage + train_percentage + val_percentage]
        sublists = []
        start_index = 0
        for percentage in cumulative_sum_percentages:
            end_index = int(data_length * percentage)
            sublists.append(self.__data[start_index:end_index])
            start_index = end_index

        return list(sublists[0]), list(sublists[1]), list(sublists[2])

    def get_unique_values(self, label: str = None) -> list[Tuple]:
        """
        :param label: nazwa etykiety, domyślnie brak
        :return: zwraca listę krotek gdzie piewszą wartością krotki jest nazwa, a drugą liczebność
        """

        try:
            indexes = []
            if label is None:
                indexes = range(0, len(self.__labels))
            else:
                indexes.append(self.__labels.index(label))

            counter = {}
            for row in self.__data:
                for index in indexes:
                    if row[index] in counter:
                        counter[row[index]] += 1
                    else:
                        counter[row[index]] = 1

            return list(counter.items())
        except ValueError:
            print(f'Brak etykiety o nazwie {label}')
            return list()

    def get_rows(self, value: str) -> list[str]:
        """
        :param value: wartość
        :return: zwraca listę wierszy, gdzie występuje zadana wartość
        """

        indexes = range(0, len(self.__labels))
        rows = list()
        for row in self.__data:
            for index in indexes:
                if row[index] == value:
                    rows.append(row)
                    break

        return rows


def read_data(filepath: str, sep: str = ' ', header: bool = True, encoding: str = 'utf-8') -> Dataset:
    """
    :param filepath: ścieżka do pliku z danymi
    :param sep: separator, który oddziela dane w wierszu, domyślnie ' '
    :param header: czy w pierwszej linii pliku z danymi znajdują się nazwy kolumn (etykiety kolumn)
    :param encoding: kodowanie pliku, domyślnie UTF-8
    :return: objekt z dataset
    """

    with open(filepath, 'rt', encoding=encoding) as file:
        labels = list()
        data = list()

        row_num = 0
        prev_row = None
        for line in file:
            row_num += 1
            row = line.rstrip().split(sep)
            data.append(row)

            if prev_row is None:
                prev_row = row
            elif len(prev_row) != len(row):
                raise Exception(f'Niezgodna liczba kolumn w wierszu {row_num}, powinno byc {len(prev_row)} a jest {len(row)}')

        if header:
            labels = data.pop(0)
        else:
            labels = [f'Column_{x}' for x in range(0, len(row))]

    return Dataset(labels, data)


def write_data(data: list[str] | list[list[str]] | list[Tuple], filepath: str, sep: str = ' ', labels: list[str] = None):
    """
    :param data: lista z danymi
    :param filepath: ścieżka do pliku gdzie mają być zapisane dane
    :param sep: separator, który oddziela dane w wierszu, domyślnie ' '
    :param labels: lista etykiet, domyślnie brak etykiet
    """

    with open(filepath, 'wt') as file:
        if labels is not None:
            line = sep.join(map(str, labels)) + '\n'
            file.write(line)

        for row in data:
            if isinstance(row, list) or isinstance(row, tuple):
                line = sep.join(map(str, row)) + '\n'
            else:
                line = row + '\n'
            file.write(line)



