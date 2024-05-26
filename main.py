import create_csv
import scrape_links
import summarize_texts

def main():
    # Step 1: Create the CSV with company links
    create_csv.create_csv()
    print("CSV with company links created.")

    # Step 2: Scrape links and gather sentences
    parent_links, child_links, parent_sentences, child_sentences = scrape_links.scrape_links()
    print("Scraping complete.")

    # Step 3: Summarize the collected sentences
    df_summary = summarize_texts.summarize_texts(parent_links, child_links, parent_sentences, child_sentences)
    print("Summarization complete. Summary saved to 'summary.csv'.")

if __name__ == "__main__":
    main()




