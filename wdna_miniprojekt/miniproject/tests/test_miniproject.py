import pytest
from miniproject.module.miniproject import read_data, write_data, Dataset

labels = list(['first_name', 'last_name', 'age', 'birthdate'])
data = list([['Jan', 'Kowalski', '25', '2000-01-01'],
             ['Jan', 'Nowak', '40', '1985-01-01'],
             ['Anna', 'Jurkiewicz', '50', '1975-01-01']])

def test_get_labels():
    print()
    dataset = Dataset(labels, list())
    assert dataset.get_labels() == labels

def test_get_labels_when_no_labels():
    print()
    dataset = Dataset(list(), list())
    assert len(dataset.get_labels()) == 0

def test_get_data():
    print()
    dataset = Dataset(list(), data)
    assert dataset.get_data() == data

def test_get_data_when_start_is_set():
    print()
    dataset = Dataset(list(), data)
    assert dataset.get_data(start=0) == data[0:]
    assert dataset.get_data(start=-1) == data[-1:]
    assert dataset.get_data(start=5) == data[5:]

def test_get_data_when_end_is_set():
    print()
    dataset = Dataset(list(), data)
    assert dataset.get_data(end=0) == data[:0]
    assert dataset.get_data(end=-1) == data[:-1]
    assert dataset.get_data(end=5) == data[:5]

def test_get_data_when_start_and_end_is_set():
    print()
    dataset = Dataset(list(), data)
    assert dataset.get_data(1, 2) == data[1:2]
    assert dataset.get_data(-1, 3) == data[-1:3]

def test_test_train_val_split_for_bad_percentage():
    print()
    dataset = Dataset(list(), data)
    test, train, val = dataset.test_train_val_split(0.10, 0.10, 0.10)
    assert test is None
    assert train is None
    assert val is None

def test_test_train_val_split_when_data_cannot_be_divided():
    print()
    dataset = Dataset(list(), data[0:2])
    test, train, val = dataset.test_train_val_split(0.20, 0.30, 0.50)
    assert test is None
    assert train is None
    assert val is None

def test_test_train_val_split_for_odd_number_of_data():
    print()
    dataset = Dataset(list(), data)
    test, train, val = dataset.test_train_val_split(0.50, 0.25, 0.25)
    assert test == data[0:1]
    assert train == data[1:2]
    assert val == data[2:3]

def test_test_train_val_split_for_even_number_of_data():
    print()
    new_data = data.copy()
    new_data.append(['Joanna', 'Frankowska', '20', '2005-01-01'])
    dataset = Dataset(list(), new_data)
    test, train, val = dataset.test_train_val_split(0.50, 0.25, 0.25)
    assert test == new_data[0:2]
    assert train == new_data[2:3]
    assert val == new_data[3:4]

def test_get_unique_values():
    print()
    unique_values = [('Jan', 2), ('Kowalski', 1), ('25', 1), ('2000-01-01', 1),
                     ('Nowak', 1), ('40', 1), ('1985-01-01', 1), ('Anna', 1),
                     ('Jurkiewicz', 1), ('50', 1), ('1975-01-01', 1)]
    dataset = Dataset(labels, data)
    assert dataset.get_unique_values() == unique_values

def test_get_unique_values_when_label_is_set():
    print()
    unique_values = [('Jan', 2), ('Anna', 1)]
    dataset = Dataset(labels, data)
    assert dataset.get_unique_values('first_name') == unique_values

def test_get_rows():
    print()
    rows = list([['Jan', 'Kowalski', '25', '2000-01-01'], ['Jan', 'Nowak', '40', '1985-01-01']])
    dataset = Dataset(labels, data)
    assert dataset.get_rows('Jan') == rows

def test_read_data():
    print()
    dataset = read_data('filename1.txt')
    assert dataset.get_labels() == labels
    assert dataset.get_data() == data

def test_read_data_when_sep_is_set():
    print()
    dataset = read_data('filename2.txt', sep=';')
    assert dataset.get_labels() == labels
    assert dataset.get_data() == data

def test_read_data_when_no_header():
    print()
    labels_no_header = list(['Column_0', 'Column_1', 'Column_2', 'Column_3'])
    dataset = read_data('filename3.txt', header=False)
    assert dataset.get_labels() == labels_no_header
    assert dataset.get_data() == data

def test_write_data():
    print()
    dataset = Dataset(labels, data)
    write_data(dataset.get_labels(), 'get_labels.txt')
    write_data(dataset.get_data(), 'get_data.txt', labels=labels)
    write_data(dataset.get_unique_values(), 'get_unique_values.txt', sep=';', labels=['word', 'count'])
    write_data(dataset.get_rows('Jan'), 'get_rows.txt', labels=labels)


if __name__ == "__main__":
    pytest.main()