from girder_worker.app import app


@app.task
def fibonacci(n):
    if n == 1 or n == 2:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)


@app.task(bind=True)
def fib_seq(task, n):
    if n < 0:
        raise Exception("Must pass in positive integer!")

    for _n in range(1, n+1):
        print "%s: %s" % (_n, fibonacci(_n))
