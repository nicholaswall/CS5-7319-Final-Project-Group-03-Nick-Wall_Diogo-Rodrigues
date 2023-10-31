from mvc.src.models.lists import ListsModel


if __name__ == "__main__":
    print("Hello world from mvc")
    created_list = ListsModel().create("test")
    print("Created list: ", created_list)
    lists = ListsModel().get_all()
    print("Lists: ", lists)
