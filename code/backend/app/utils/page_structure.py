from app.utils.style import PAGE_STYLE

ROOT_PAGE = f"""
<html>
    <head>{PAGE_STYLE}</head>
    <body>
        <h1>Wunderbar Dashboard API</h1>
        <p>Status: running</p>
    </body>
</html>
"""

#region Exception Pages

EXCEPTION_404_PAGE = f"""
<html>
    <head>{PAGE_STYLE}</head>
    <body>
        <h1>Nothing to see here</h1>
    </body>
</html>
"""

EXCEPTION_500_PAGE = f"""
<html>
    <head>{PAGE_STYLE}</head>
    <body>
        <h1>Something went wrong</h1>
    </body>
</html>
"""

#endregion