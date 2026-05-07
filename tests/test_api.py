import json

def test_create_book(client):
    data = {
        "title": "1984",
        "author": "George Orwell",
        "description": "Dystopian novel",
        "status": "наявні в бібліотеці",
        "year": 1949
    }
    response = client.post('/books', json=data)
    assert response.status_code == 201
    assert "1984" in response.get_data(as_text=True)

def test_get_books(client):
    data = {
        "title": "1984",
        "author": "George Orwell",
        "description": "Dystopian novel",
        "status": "наявні в бібліотеці",
        "year": 1949
    }
    client.post('/books', json=data)
    response = client.get('/books')
    assert response.status_code == 200
    assert "1984" in response.get_data(as_text=True)

def test_get_book(client):
    data = {
        "title": "1984",
        "author": "George Orwell",
        "description": "Dystopian novel",
        "status": "наявні в бібліотеці",
        "year": 1949
    }
    post_response = client.post('/books', json=data)
    book_id = json.loads(post_response.data)['_id']
    
    response = client.get(f'/books/{book_id}')
    assert response.status_code == 200
    assert "1984" in response.get_data(as_text=True)

def test_delete_book(client):
    data = {
        "title": "1984",
        "author": "George Orwell",
        "description": "Dystopian novel",
        "status": "наявні в бібліотеці",
        "year": 1949
    }
    post_response = client.post('/books', json=data)
    book_id = json.loads(post_response.data)['_id']
    
    delete_response = client.delete(f'/books/{book_id}')
    assert delete_response.status_code == 204
    
    get_response = client.get(f'/books/{book_id}')
    assert get_response.status_code == 404