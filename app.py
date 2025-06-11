from flask import Flask, render_template, request
import numpy as np
import pickle

# Load the pre-trained model and data

popular_book =open('E:/Book Reccomendation/Reccomand frontend and server/popular.pkl', 'rb')
# Use 'rb' mode to read the pickle file in binary format
popular_books = pickle.load(popular_book)

pt = pickle.load(open('E:/Book Reccomendation/Reccomand frontend and server/pt.pkl', 'rb'))
books = pickle.load(open('E:/Book Reccomendation/Reccomand frontend and server/books.pkl', 'rb'))

similarity_score = pickle.load(open('E:/Book Reccomendation/Reccomand frontend and server/similarity_score.pkl', 'rb'))


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html",
                        book_name=list(popular_books['Book-Title'].values),
                        author_name=list(popular_books['Book-Author'].values),
                        image=list(popular_books['Image-URL-M'].values),
                        rating=list(popular_books['avg_rating'].values),
                        votes=list(popular_books['Num-Ratings'].values))


@app.route("/recommend")
def recommand():
    return render_template("recommend.html",
                        book_name=list(popular_books['Book-Title'].values),
                        author_name=list(popular_books['Book-Author'].values),
                        image=list(popular_books['Image-URL-M'].values),
    )

@app.route("/recommend_book",methods=['POST'])
def recommend_books():
    book_name = request.form.get('user_input')

    # Get the index of the book
    index = np.where(pt.index == book_name)[0][0]
    # Get the similarity scores for the book
    distance = similarity_score[index]
    
    # Get the indices of the books sorted by similarity score
    similar_item = sorted(list(enumerate(distance)), key=lambda x: x[1], reverse=True)[1:7]  # Exclude the book itself

    data =[]
    
    for i in similar_item:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.append(temp_df.drop_duplicates("Book-Title")['Book-Title'].values[0])
        item.append(temp_df.drop_duplicates("Book-Title")['Book-Author'].values[0])
        item.append(temp_df.drop_duplicates("Book-Title")['Image-URL-M'].values[0])

        data.append(item)

    book_name = [item[0] for item in data]
    author_name = [item[1] for item in data]
    image = [item[2] for item in data]

    return render_template("recommend.html",
                           book_name=book_name,
                           author_name=author_name,
                           image=image)

if __name__ == "__main__":
    app.run(debug=True)
