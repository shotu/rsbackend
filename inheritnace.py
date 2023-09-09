class ParentClass:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def method1(self):
        # Parent class method
        pass

    def method2(self):
        # Parent class method
        print("method2 parent called",self.arg3)
        
        pass

class ChildClass(ParentClass):
    def __init__(self, arg1, arg2, arg3):
        # Call the parent class's __init__ method
        # super().__init__(arg1, arg2)

        # Perform additional initialization for the child class
        self.arg3 = arg3

    # Child class-specific method
    def child_method(self):
        print("child method")
        pass

# Creating an instance of ChildClass
child_obj = ChildClass("value1", "value2", "value3")

child_obj.child_method()
child_obj.method2()