
function Footer({ myprofile }) {
  return (
    <footer className="footer">
      <p>
        © {new Date().getFullYear()} Prashant Shah. All rights reserved.
      </p>

      <div className="footer-links">
        <a
          href={myprofile?.github_url}
          target="_blank"
          rel="noopener noreferrer"
        >
          GitHub ↗
        </a>

        <a
          href={myprofile?.linkedin_url}
          target="_blank"
          rel="noopener noreferrer"
        >
          LinkedIn ↗
        </a>
      </div>
    </footer>
  );
}

export default Footer;
