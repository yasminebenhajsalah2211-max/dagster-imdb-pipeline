def test_transform():
    import pandas as pd
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    from dagster_project.assets import clean_movies

    df = pd.DataFrame({
        "rating": ["9.1", "8.5"],
        "year": ["2000", "2010"]
    })

    result = clean_movies(df)

    assert result["rating"].dtype != object
    assert result["year"].dtype != object