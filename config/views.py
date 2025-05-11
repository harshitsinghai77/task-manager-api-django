# config/views.py
from django.http import HttpResponse

def welcome_page(request):
    return HttpResponse("""
       <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Task Manager API</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    background-color: #f9f9f9;
                    color: #333;
                    padding: 40px;
                    max-width: 700px;
                    margin: auto;
                }
                h1 {
                    color: #2c3e50;
                }
                a {
                    color: #3498db;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
                .info {
                    margin-top: 20px;
                    padding: 10px 20px;
                    background: #ffffff;
                    border: 1px solid #e1e1e1;
                    border-radius: 6px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                }
                .info p {
                    margin: 10px 0;
                }
                code {
                    background-color: #f4f4f4;
                    padding: 2px 6px;
                    border-radius: 4px;
                }
            </style>
        </head>
        <body>
            <h1>👋 Welcome to the Task Manager API</h1>
            <div class="info">
                <p><strong>Base URL:</strong> All API endpoints start with <code>/api/</code>. For example: <code>/api/tasks/</code></p>
                <p><strong>Swagger UI:</strong> <a href="/api/docs/">/api/docs/</a></p>
                <p><strong>ReDoc:</strong> <a href="/api/redoc/">/api/redoc/</a></p>
                <p><strong>Admin Panel:</strong> <a href="/admin/">/admin/</a> (username: <strong>user</strong>, password: <strong>password</strong>)</p>
            </div>
        </body>
        </html>
    """)
