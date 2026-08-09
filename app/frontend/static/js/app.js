const API_BASE = "/api/v1";

async function fetchPreview(file, fileType) {
  let endpoint;

  if (fileType === "image") endpoint = `${API_BASE}/images/preview`;
  else if (fileType === "document") endpoint = `${API_BASE}/documents/preview`;
  else return null;

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(endpoint, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    let message = `Preview failed with status ${response.status}.`;
    try {
      const data = await response.json();
      message = data.error || message;
    } catch {}

    throw new Error(message);
  }

  const blob = await response.blob();
  return {
    url: URL.createObjectURL(blob),
    type: blob.type,
  };
}

function openFileDatabase() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("blurStuff", 1);
    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains("files")) db.createObjectStore("files");
    };

    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
  });
}

async function storeUploadedFile(file) {
  const db = await openFileDatabase();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction("files", "readwrite");
    const store = transaction.objectStore("files");
    store.put(
      {
        file: file,
        createdAt: Date.now(),
      },
      "current",
    );

    transaction.oncomplete = () => {
      db.close();
      resolve();
    };

    transaction.onerror = () => {
      db.close();
      reject(transaction.error);
    };
  });
}

async function getCurrentUpload() {
  const db = await openFileDatabase();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction("files", "readonly");
    const store = transaction.objectStore("files");
    const request = store.get("current");
    request.onsuccess = () => {
      db.close();

      const entry = request.result;
      if (!entry) {
        resolve(null);
        return;
      }

      const maxAge = 10 * 60 * 1000;
      if (Date.now() - entry.createdAt > maxAge) {
        deleteUploadedFile().finally(() => resolve(null));
        return;
      }

      resolve(entry);
    };

    request.onerror = () => {
      db.close();
      reject(request.error);
    };
  });
}

async function deleteUploadedFile() {
  const db = await openFileDatabase();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction("files", "readwrite");
    const store = transaction.objectStore("files");
    store.delete("current");

    transaction.oncomplete = () => {
      db.close();
      resolve();
    };

    transaction.onerror = () => {
      db.close();
      reject(transaction.error);
    };
  });
}

async function storeDetectionResult(detections) {
  const db = await openFileDatabase();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction("files", "readwrite");
    const store = transaction.objectStore("files");
    const request = store.get("current");

    request.onsuccess = () => {
      const entry = request.result;
      if (!entry) {
        reject(new Error("No uploaded file found."));
        return;
      }

      store.put(
        {
          ...entry,
          detections,
          detectedAt: Date.now(),
        },
        "current",
      );
    };

    request.onerror = () => {
      reject(request.error);
    };

    transaction.oncomplete = () => {
      db.close();
      resolve();
    };

    transaction.onerror = () => {
      db.close();
      reject(transaction.error);
    };
  });
}

function uploadBox() {
  return {
    isDragging: false,
    handleFile(event) {
      const file = event.target.files?.[0];
      if (!file) return;

      this.upload(file);
    },
    handleDrop(event) {
      this.isDragging = false;

      const file = event.dataTransfer.files?.[0];
      if (!file) return;

      this.upload(file);
    },
    async upload(file) {
      try {
        await storeUploadedFile(file);
        window.location.href = "/detect";
      } catch (error) {
        console.error("Failed to store file:", error);
      }
    },
  };
}

function anonymizeApp() {
  return {
    file: null,
    previewUrl: null,
    fileType: null,
    previewType: null,
    isPreviewLoading: false,
    isDragging: false,
    detections: null,
    isDetecting: false,
    detectionError: null,
    targets: {
      faces: true,
      plates: false,
      text: false,
      pii: false,
    },
    mode: "blur",
    canDetect() {
      return (
        this.file &&
        (this.targets.faces ||
          this.targets.plates ||
          this.targets.text ||
          this.targets.pii)
      );
    },
    async init() {
      try {
        const storedFile = await getCurrentUpload();
        if (!storedFile) return;

        await this.setFile(storedFile.file);
      } catch (error) {
        console.error("Failed to load uploaded file:", error);
      }
    },
    async handleFile(event) {
      const file = event.target.files?.[0];
      if (!file) return;

      try {
        await storeUploadedFile(file);

        await this.setFile(file);
        event.target.value = "";

        this.detections = null;
        this.detectionError = null;
      } catch (error) {
        console.error("Failed to store file:", error);
        this.detectionError = "Failed to prepare the file.";
      }
    },
    async handleDrop(event) {
      this.isDragging = false;

      const file = event.dataTransfer.files?.[0];
      if (!file) return;

      try {
        await storeUploadedFile(file);

        await this.setFile(file);
        this.detections = null;
        this.detectionError = null;
      } catch (error) {
        console.error("Failed to store file:", error);
        this.detectionError = "Failed to prepare the file.";
      }
    },
    async setFile(file) {
      this.file = file;

      if (this.previewUrl) {
        URL.revokeObjectURL(this.previewUrl);
        this.previewUrl = null;
      }

      this.isPreviewLoading = false;

      const extension = this.getExtension(file);
      const previewableImages = ["jpg", "jpeg", "png", "webp", "gif"];
      const videoFormats = ["mp4", "mov", "avi", "mkv", "webm"];
      const imageFormats = [
        ...previewableImages,
        "tif",
        "tiff",
        "heic",
        "heif",
      ];

      if (previewableImages.includes(extension)) {
        this.fileType = "image";
        this.previewType = "image";

        this.previewUrl = URL.createObjectURL(file);
      } else if (videoFormats.includes(extension)) {
        this.fileType = "video";
        this.previewType = "video";

        this.previewUrl = URL.createObjectURL(file);
      } else if (imageFormats.includes(extension)) {
        this.fileType = "image";
        this.previewType = "image";
        this.isPreviewLoading = true;

        try {
          const preview = await fetchPreview(file, "image");
          this.previewUrl = preview.url;
        } catch (error) {
          console.error("Failed to generate image preview:", error);
          this.previewType = "file";
          this.detectionError = "Failed to generate a preview.";
        } finally {
          this.isPreviewLoading = false;
        }
      } else {
        this.fileType = "document";
        this.previewType = "pdf";
        this.isPreviewLoading = true;

        try {
          const preview = await fetchPreview(file, "document");
          this.previewUrl = preview.url;
        } catch (error) {
          console.error("Failed to generate document preview:", error);
          this.previewType = "file";
          this.detectionError = "Failed to generate a document preview.";
        } finally {
          this.isPreviewLoading = false;
        }
      }
    },
    getExtension(file) {
      return file.name.split(".").pop().toLowerCase();
    },
    fileTypeLabel() {
      if (!this.file) return "";

      const extension = this.getExtension(this.file).toUpperCase();
      if (this.fileType === "image") return `${extension} Image`;
      if (this.fileType === "video") return `${extension} Video`;

      return `${extension} Document`;
    },
    formatSize(bytes) {
      if (!bytes) return "";
      if (bytes < 1024) return `${bytes} B`;
      if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;

      return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    },
    getSelectedTargets() {
      const selected = [];
      if (this.targets.faces) selected.push("faces");
      if (this.targets.plates) selected.push("plates");
      if (this.targets.text) selected.push("text");
      if (this.targets.pii) selected.push("pii");

      return selected;
    },
    getDetectionEndpoint() {
      if (this.fileType === "image") return `${API_BASE}/images/detect`;
      if (this.fileType === "video") return `${API_BASE}/videos/detect`;
      if (this.fileType === "document") return `${API_BASE}/documents/detect`;

      return null;
    },
    async detect() {
      if (!this.canDetect()) return;

      this.isDetecting = true;
      this.detectionError = null;
      this.detections = null;

      try {
        const endpoint = this.getDetectionEndpoint();
        if (!endpoint) throw new Error("Unsupported file type.");

        const selectedTargets = this.getSelectedTargets();
        if (selectedTargets.length === 0)
          throw new Error("Select at least one detection target.");

        const formData = new FormData();
        formData.append("file", this.file);

        const params = new URLSearchParams();
        params.set("targets", selectedTargets.join(","));

        const response = await fetch(`${endpoint}?${params.toString()}`, {
          method: "POST",
          body: formData,
        });

        let data;
        try {
          data = await response.json();
        } catch {
          throw new Error(`Detection failed with status ${response.status}.`);
        }

        if (!response.ok)
          throw new Error(
            data.error || `Detection failed with status ${response.status}.`,
          );

        await storeDetectionResult(data);
        window.location.href = "/results";
      } catch (error) {
        console.error("Detection failed:", error);
        this.detectionError =
          error.message || "Something went wrong while detecting the file.";
      } finally {
        this.isDetecting = false;
      }
    },
  };
}

function resultsApp() {
  return {
    file: null,
    previewUrl: null,
    fileType: null,
    detections: null,
    isLoading: true,
    error: null,
    imageDimensions: null,
    videoDuration: null,
    showDetections: true,
    async init() {
      try {
        const storedFile = await getCurrentUpload();

        if (!storedFile) {
          this.error = "No file found.";
          this.isLoading = false;

          window.location.replace("/detect");
          return;
        }

        this.file = storedFile.file;
        this.detections = storedFile.detections || null;
        await this.setPreview(this.file);
      } catch (error) {
        console.error("Failed to load results:", error);
        this.error = "Failed to load the file.";
      } finally {
        this.isLoading = false;
      }
    },
    async setPreview(file) {
      if (!file) return;

      if (this.previewUrl) {
        URL.revokeObjectURL(this.previewUrl);
        this.previewUrl = null;
      }

      const extension = this.getExtension(file);
      const browserPreviewableImages = ["jpg", "jpeg", "png", "webp", "gif"];
      const imageFormats = [
        ...browserPreviewableImages,
        "tif",
        "tiff",
        "heic",
        "heif",
      ];

      const videoFormats = ["mp4", "mov", "avi", "mkv", "webm"];
      const documentFormats = [
        "pdf",
        "doc",
        "docx",
        "xls",
        "xlsx",
        "ppt",
        "pptx",
      ];

      if (imageFormats.includes(extension)) {
        this.fileType = "image";

        if (browserPreviewableImages.includes(extension)) {
          this.previewUrl = URL.createObjectURL(file);
        } else {
          try {
            const preview = await fetchPreview(file, "image");
            this.previewUrl = preview.url;
          } catch (error) {
            console.error("Failed to generate image preview:", error);
            this.error = "Failed to generate image preview.";
          }
        }
      } else if (videoFormats.includes(extension)) {
        this.fileType = "video";
        this.previewUrl = URL.createObjectURL(file);
      } else if (documentFormats.includes(extension)) {
        this.fileType = "pdf";

        try {
          const preview = await fetchPreview(file, "document");
          this.previewUrl = preview.url;
        } catch (error) {
          console.error("Failed to generate document preview:", error);
          this.error = "Failed to generate document preview.";
        }
      } else if (file.type.startsWith("image/")) {
        this.fileType = "image";

        try {
          const preview = await fetchPreview(file, "image");
          this.previewUrl = preview.url;
        } catch (error) {
          console.error("Failed to generate image preview:", error);
          this.error = "Failed to generate image preview.";
        }
      } else {
        this.fileType = "document";

        try {
          const preview = await fetchPreview(file, "document");
          this.previewUrl = preview.url;
        } catch (error) {
          console.error("Failed to generate document preview:", error);
          this.error = "Failed to generate document preview.";
        }
      }
    },
    getExtension(file) {
      if (!file?.name) return "";
      return file.name.split(".").pop().toLowerCase();
    },
    fileTypeLabel() {
      if (!this.file) return "";

      const extension = this.getExtension(this.file).toUpperCase();
      if (this.fileType === "image") return `${extension} Image`;
      if (this.fileType === "video") return `${extension} Video`;
      if (this.fileType === "pdf") return "PDF Document";

      return `${extension} Document`;
    },
    formatSize(bytes) {
      if (!bytes) return "";

      if (bytes < 1024) return `${bytes} B`;
      if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
      if (bytes < 1024 * 1024 * 1024)
        return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;

      return `${(bytes / (1024 * 1024 * 1024)).toFixed(1)} GB`;
    },
    formatDuration(seconds) {
      if (!seconds || !Number.isFinite(seconds)) return "";

      const totalSeconds = Math.floor(seconds);
      const minutes = Math.floor(totalSeconds / 60);
      const remainingSeconds = totalSeconds % 60;
      return `${String(minutes).padStart(2, "0")}:${String(
        remainingSeconds,
      ).padStart(2, "0")}`;
    },
    handleImageLoad(event) {
      const image = event.target;
      this.imageDimensions = `${image.naturalWidth} × ${image.naturalHeight}`;
    },
    handleVideoMetadata(event) {
      this.videoDuration = event.target.duration;
    },
    changeFile() {
      this.$refs.replaceInput.click();
    },
    async handleReplacement(event) {
      const file = event.target.files?.[0];
      if (!file) return;

      try {
        await storeUploadedFile(file);

        this.file = file;
        this.detections = null;
        await this.setPreview(file);

        window.location.href = "/detect";
      } catch (error) {
        console.error("Failed to replace file:", error);
        this.error = "Failed to replace the file.";
      }
    },
    visibleDetections() {
      if (!this.detections) return [];
      if (Array.isArray(this.detections)) return this.detections;

      return [];
    },
    boxStyle(detection) {
      if (!detection) return {};
      const width = detection.x2 - detection.x1;
      const height = detection.y2 - detection.y1;

      return {
        left: `${detection.x1 * 100}%`,
        top: `${detection.y1 * 100}%`,
        width: `${width * 100}%`,
        height: `${height * 100}%`,
      };
    },
    destroy() {
      if (this.previewUrl) URL.revokeObjectURL(this.previewUrl);
    },
    isDocument() {
      return this.fileType === "document" || this.fileType === "pdf";
    },
  };
}
