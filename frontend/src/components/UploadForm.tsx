function UploadForm() {
  return (
    <form className="glass-form">
      <div className="form-group">
        <label htmlFor="title" className="input-label">
          Title
        </label>
        <input
          type="text"
          id="title"
          className="text-input"
          placeholder="Enter project title..."
        />
      </div>

      <div className="form-group">
        <label htmlFor="file-upload" className="input-label">
          Upload Asset
        </label>
        <input type="file" id="file-upload" className="file-input" />
      </div>

      <button type="submit" className="submit-button">
        Upload File
      </button>
    </form>
  );
}

export default UploadForm;
