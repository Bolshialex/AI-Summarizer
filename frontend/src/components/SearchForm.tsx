function SearchForm() {
  return (
    <form className="search-form">
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
