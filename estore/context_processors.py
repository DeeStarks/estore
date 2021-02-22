def global_variable(request):
    review_ranges = {
        'zero': 0,
        'one': range(1, 20),
        'two': range(20, 40),
        'three': range(40, 60),
        'four': range(60, 80),
        'five': range(80, 101),
    }

    return { 
        'review_ranges': review_ranges,
    }