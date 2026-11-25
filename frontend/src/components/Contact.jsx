
import { useEffect, useRef, useState } from "react";

// Only fall back to localhost during local development. In a production build
// a missing VITE_API_BASE_URL must not turn into requests to the visitor's
// own machine (which show up as an unhelpful "Failed to fetch").
const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  (import.meta.env.DEV ? "http://127.0.0.1:8000" : "")
).replace(/\/+$/, "");

// The backend is only needed for the contact form now. When this page is opened
// after the free Render service has slept, waking it takes ~30s. We start that
// wake-up as soon as the contact section is about to be seen, so by the time a
// visitor types a message and submits, the backend is already warm.
let backendWarmed = false;

function Contact({ formData, setFormData }) {
  const sectionRef = useRef(null);
  const [isSending, setIsSending] = useState(false);//setIsSending(true) means the request has started setIsSending(false) means the request has finished
  const [status, setStatus] = useState({
    type: "",
    message: "",
  });

  useEffect(() => {
    if (backendWarmed || !API_BASE_URL) return;

    const warmBackend = () => {
      if (backendWarmed) return;
      backendWarmed = true;

      // Fire-and-forget: we only care that the container boots.
      fetch(`${API_BASE_URL}/api/profile/`, { cache: "no-store" }).catch(
        () => {},
      );
    };

    const node = sectionRef.current;
    if (!node || !("IntersectionObserver" in window)) {
      warmBackend();
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((entry) => entry.isIntersecting)) {
          warmBackend();
          observer.disconnect();
        }
      },
      { rootMargin: "300px" },
    );

    observer.observe(node);
    return () => observer.disconnect();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus({ type: "", message: "" });

    if (!API_BASE_URL) {
      setStatus({
        type: "error",
        message: "Contact form is not configured. Please email me directly.",
      });
      return;
    }

    setIsSending(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/contact/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || "Something went wrong");
      }
      setStatus({
        type: "success",
        message: data.message || "Message sent successfully",
      });
      setFormData({
        name: "",
        email: "",
        message: "",
      });
    } catch (error) {
      console.error("Error sending message:", error);

      // A "Failed to fetch" TypeError means the request never reached the
      // server (offline, CORS, DNS, or backend asleep). Give a clearer hint
      // than the browser's default wording.
      const isNetworkError =
        error instanceof TypeError || error.message === "Failed to fetch";

      setStatus({
        type: "error",
        message: isNetworkError
          ? "Could not reach the server. Please check your connection and try again."
          : error.message || "Failed to send message",
      });
    } finally {
      setIsSending(false);
    }
  };

  return (
    <section className="contact" id="contact" ref={sectionRef}>
      <div className="section-heading">
        <p className="eyebrow">GET IN TOUCH</p>
        <h2>Let's work together.</h2>
        <p>
          Have a project in mind, an opportunity, or just want to connect? Feel
          free to send me a message.
        </p>
      </div>

      <form className="contact-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Your name"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          required
          disabled={isSending}
        />

        <input
          type="email"
          placeholder="Your email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          required
          disabled={isSending}
        />

        <textarea
          placeholder="Your message"
          rows="5"
          value={formData.message}
          onChange={(e) =>
            setFormData({ ...formData, message: e.target.value })
          }
          required
          disabled={isSending}
        />

        <button type="submit" disabled={isSending}>
          {isSending ? "Sending.." : "Send Message ↗"}
        </button>
        {status.message && (
          <p
            className={`form-status ${status.type}`}
            role="status"
            aria-live="polite"
          >
            {status.message}
          </p>
        )}
      </form>
    </section>
  );
}

export default Contact;
