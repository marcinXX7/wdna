from miniproject.module.miniproject import read_data, write_data

if __name__ == "__main__":
    dataset = read_data('winequality-red.csv', sep=';')
    print(dataset.get_labels())
    print(dataset.get_data(1, 5))
    print(dataset.get_unique_values('"alcohol"'))
    print(dataset.get_rows('10.55'))
    test, train, val = dataset.test_train_val_split(0.5, 0.4, 0.1)
    write_data(test, 'test_values.txt', sep=';', labels=dataset.get_labels())
    write_data(train, 'train_values.txt', sep=';', labels=dataset.get_labels())
    write_data(val, 'val_values.txt', sep=';', labels=dataset.get_labels())
