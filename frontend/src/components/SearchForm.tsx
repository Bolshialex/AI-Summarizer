import { useRef, type SubmitEvent } from "react";

function SearchForm() {
  const formRef = useRef<HTMLFormElement>(null);

  const handleSubmit = async (event: SubmitEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      const formData = new FormData(event.currentTarget);
      const searchTerm = formData.get("search") as string;

      console.log(searchTerm);
      await new Promise((resolve) => setTimeout(resolve, 1500));

      formRef.current?.reset();
    } catch {
      console.log("error");
    } finally {
      console.log("");
    }
  };
  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <div className="search-input-wrapper">
        <label htmlFor="search" className="form-label">
          Enter a topic
        </label>
        <input
          type="text"
          name="search"
          id="search"
          className="form-input"
          placeholder="What are you looking for?"
        />
      </div>

      <div className="button-group">
        <button type="submit" className="submit-button">
          Search
        </button>
      </div>
    </form>
  );
}

export default SearchForm;
