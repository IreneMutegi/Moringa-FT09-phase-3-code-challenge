from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Create tables or handle other initializations
    create_tables()

    # Collect input from the user
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Check for empty inputs
    if not (author_name and magazine_name and magazine_category and article_title and article_content):
        print("All fields are required. Please try again.")
        return

    try:
        # Create Author, Magazine, and Article objects
        author = Author(None, name=author_name)
        magazine = Magazine(name=magazine_name, category=magazine_category)
        article = Article(author_id=author.id, magazine_id=magazine.id, title=article_title, content=article_content)
        # Save them to the database
        author.save()
        magazine.save()  # Now works because `save` is implemented
        article.save()
    
    except ValueError as e:
        print(f"Error: {str(e)}")
        return

    try:
        # Display results
        print("\nMagazines:")
        magazines = Magazine.get_all()  # This should now work if get_all() is defined correctly
        for magazine in magazines:
            print(f"Magazine ID: {magazine.id}, Name: {magazine.name}, Category: {magazine.category}")

        print("\nAuthors:")
        authors = Author.get_all()  # Assuming this method exists in the Author class
        for author in authors:
            print(f"Author ID: {author.id}, Name: {author.name}")

        print("\nArticles:")
        articles = Article.get_all()  # Assuming this method exists in the Article class
        for article in articles:
            print(f"Article ID: {article.id}, Title: {article.title}, Content: {article.content}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return

if __name__ == "__main__":
    main()
