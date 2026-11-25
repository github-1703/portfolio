// Turns a stored image value into a usable URL.
//
// - Absolute URLs (Cloudinary) are returned with an optimization transform
//   inserted, so we never download the full-size original.
// - Relative paths fall back to the legacy Django media root.

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "").replace(
  /\/+$/,
  "",
);

const DEFAULT_TRANSFORM = "f_auto,q_auto:good,w_900,c_limit";

function isCloudinary(path) {
  return (
    /^https?:\/\//i.test(path) &&
    path.includes("res.cloudinary.com") &&
    path.includes("/upload/")
  );
}

export function getImageUrl(path, { width, transform } = {}) {
  if (!path) return null;

  const appliedTransform =
    transform ||
    (width
      ? `f_auto,q_auto:good,w_${width},c_limit`
      : DEFAULT_TRANSFORM);

  if (/^https?:\/\//i.test(path)) {
    if (isCloudinary(path)) {
      const [base, rest] = path.split("/upload/");
      const firstSegment = rest.split("/")[0];

      // Already has a transformation, or is a version segment (v123...).
      const alreadyTransformed =
        firstSegment.includes("_") && !firstSegment.startsWith("v");

      if (!alreadyTransformed) {
        return `${base}/upload/${appliedTransform}/${rest}`;
      }
    }

    return path;
  }

  return `${API_BASE_URL}/${path.replace(/^\/+/, "")}`;
}

// Builds a responsive srcSet (e.g. 1x/2x) from an existing Cloudinary URL by
// swapping the width parameter. Returns undefined for non-Cloudinary paths.
export function getImageSrcSet(path, widths = []) {
  if (!path || widths.length === 0 || !isCloudinary(path)) return undefined;

  return widths
    .map((width) => {
      let url;

      if (/w_\d+/.test(path)) {
        url = path.replace(/w_\d+/, `w_${width}`);
      } else {
        url = getImageUrl(path, { width });
      }

      return `${url} ${width}w`;
    })
    .join(", ");
}
