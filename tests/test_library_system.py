import unittest
import library_system

class TestLibrarySystem(unittest.TestCase):
    @classmethod                                                # Must be decorated as class method 
    def setUpClass(cls): 
        library_system.books.clear()
        library_system.borrowed.clear()                                       # setUpClass() class method is called before the tests (in an individual class) are run. It has class as the only argument
        library_system.books.append ({"author":"Roger Burke", "title": "Rose", "category": "Romance", "available": True})
        library_system.books.append ({"author":"David Ram", "title": "Yellow", "category":"Fiction", "available": True})
        return super().setUpClass()
    

    @classmethod                                                # Must be decorated as class method
    def tearDownClass(cls):                                     # tearDownClass() class method is called after all tests (in an individual class) have run. It has class as the only argument
        print("\n\nTear down a class")
        print("Releasing the resources")
        return super().tearDownClass()
    
    # ----- ADD / VIEW BOOKS -----

    def test_book_added(self):
        self.assertEqual(len(library_system.books), 2)

    def test_view_books(self):
        self.assertTrue(len(library_system.books) > 0)

     # ----- SEARCH BOOK -----
    def test_search_books(self):
        self.assertEqual(library_system.books[0]["title"], "Rose")
    

    # -----RETURN BOOK -------
    def test_return_books(self):
        library_system.books[0]["available"] = True
        self.assertTrue(library_system.books[0]["available"])


    # -----AVAILABILITY BOOK -------   
    def test_book_availablity(self):
        self.assertTrue(library_system.books[0]["available"])

    # -----BORROW BOOK -------
    def test_borrow_books(self):
        library_system.books[0]["available"] = False
        self.assertFalse(library_system.books[0]["available"])
    
        # -----DELETE BOOK -------
    def test_delete_books(self):
        library_system.books.pop()
        self.assertEqual(len(library_system.books), 1)

if __name__ == "__main__":
    unittest.main()