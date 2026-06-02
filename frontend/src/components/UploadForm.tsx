import { useState, useRef, type SubmitEvent } from "react";

type StatusMessage = {
  type: "success" | "error";
  text: string;
};

function UploadForm() {
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<StatusMessage | null>(null);

  const formRef = useRef<HTMLFormElement>(null);

  const handleSubmit = async (event: SubmitEvent<HTMLFormElement>) => {
    event.preventDefault();

    setIsLoading(true);
    setMessage(null);

    try {
      await new Promise((resolve) => setTimeout(resolve, 1500));

      const isSuccess = Math.random() >= 0.5;

      if (!isSuccess) {
        throw new Error("Simulated upload failure");
      }

      setMessage({ type: "success", text: "Asset uploaded successfully!" });
      formRef.current?.reset();
    } catch {
      setMessage({ type: "error", text: "Upload failed. Please try again." });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form className="glass-form" onSubmit={handleSubmit} ref={formRef}>
      {message && (
        <div
          className={`status-message ${message.type === "success" ? "success-text" : "error-text"}`}
          style={{
            color: message.type === "success" ? "green" : "red",
            marginBottom: "1rem",
            fontWeight: "bold",
          }}
        >
          {message.text}
        </div>
      )}

      <div className="form-group">
        <label htmlFor="title" className="input-label">
          Title
        </label>
        <input
          type="text"
          id="title"
          className="text-input"
          placeholder="Enter project title..."
          disabled={isLoading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="file-upload" className="input-label">
          Upload Asset
        </label>
        <input
          type="file"
          id="file-upload"
          className="file-input"
          disabled={isLoading}
        />
      </div>

      <button type="submit" className="submit-button" disabled={isLoading}>
        {isLoading ? "Uploading..." : "Upload File"}
      </button>
    </form>
  );
}

export default UploadForm;
