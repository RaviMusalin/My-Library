const headers = {
    'Content-Type': 'application/json'
}

function ownedBook(event, title, author, isbn, bookCover) {
    let body = {
        title: title,
        author:author,
        isbn:isbn,
        book_cover:bookCover
    }
    fetch('/saved_to_own', {
        method: "POST",
        body: JSON.stringify(body),
        headers: headers
    })
    .then(res => res.text())
    .then(resText => {
        event.target.disabled = true;
        alert(resText)
    })
    
    console.log(title)
    console.log(author)
}
