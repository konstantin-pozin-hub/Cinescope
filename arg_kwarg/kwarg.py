# def greet(**kwargs):
#     if "name" in kwargs:
#         print(f"Hello, {kwargs['name']}!")
#     else:
#         print("Hello, stranger!")
#
# greet(name = "Alex", age = 24 )

# def create_dict(**kwargs):
#     return kwargs
# print(create_dict(a=1, b=2, c=3))


def create_list(*args):
    print(args)


create_list(1, 2, 3, 4, 5, 6, 7, 8, 1, 1, 11, )
