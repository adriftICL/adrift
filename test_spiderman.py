from spiderman import get, post, run

class Test:
    @get('/x')
    def some_func():
        some_local = "some_local_var"
        pass

run()
