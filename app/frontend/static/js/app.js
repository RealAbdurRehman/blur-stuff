const API_BASE = "/api/v1";

document.addEventListener("alpine:init", () => {
  Alpine.store("notifications", {
    items: [],
    show(message, type = "error", duration = 5000) {
      const id = Date.now() + Math.random();
      this.items.push({
        id,
        message,
        type,
        visible: false,
      });

      requestAnimationFrame(() => {
        const notification = this.items.find((item) => item.id === id);
        if (notification) notification.visible = true;
      });

      if (duration > 0) setTimeout(() => this.remove(id), duration);
    },
    success(message, duration = 4000) {
      this.show(message, "success", duration);
    },
    error(message, duration = 4000) {
      this.show(message, "error", duration);
    },
    warning(message, duration = 4000) {
      this.show(message, "warning", duration);
    },
    info(message, duration = 4000) {
      this.show(message, "info", duration);
    },
    remove(id) {
      const notification = this.items.find((item) => item.id === id);
      if (!notification || !notification.visible) return;
      notification.visible = false;
    },
    clear() {
      this.items = [];
    },
  });
});

function getErrorMessage(error, fallback = "Something went wrong.") {
  if (error instanceof Error && error.message) return error.message;
  return fallback;
}

function notifyError(error, fallback = "Something went wrong.") {
  console.error(error);
  const message = getErrorMessage(error, fallback);

  Alpine.store("notifications").error(message);
  return message;
}

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

async function storeProcessedFile(blob, outputName) {
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
          processedFile: blob,
          outputName,
          processedAt: Date.now(),
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
        notifyError(error, "Failed to upload the file.");
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
        this.detectionError = notifyError(
          error,
          "Failed to load the uploaded file.",
        );
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
        this.detectionError = notifyError(error, "Failed to prepare the file.");
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
        this.detectionError = notifyError(error, "Failed to prepare the file.");
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
          this.previewType = "file";
          this.detectionError = notifyError(
            error,
            "Failed to generate an image preview.",
          );
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
          this.previewType = "file";
          this.detectionError = notifyError(
            error,
            "Failed to generate a document preview.",
          );
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
    hasDetections(detections) {
      if (!detections) return false;
      if (Array.isArray(detections)) {
        return detections.some((result) => {
          if (!result) return false;
          if (result.detections)
            return Object.values(result.detections).some(
              (items) => Array.isArray(items) && items.length > 0,
            );

          return ["faces", "plates", "text", "pii"].some(
            (target) =>
              Array.isArray(result[target]) && result[target].length > 0,
          );
        });
      }

      return ["faces", "plates", "text", "pii"].some(
        (target) =>
          Array.isArray(detections[target]) && detections[target].length > 0,
      );
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
        const hasDetections = this.hasDetections(data);
        if (!hasDetections) {
          Alpine.store("notifications").info(
            "No sensitive content of the selected type was detected in this file.",
          );
          return;
        }

        window.location.href = "/results";
      } catch (error) {
        this.detectionError = notifyError(
          error,
          "Something went wrong while detecting the file.",
        );
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
    cropUrls: {},
    documentPages: {},
    selectedDetections: [],
    mode: "blur",
    padding: 20,
    isProcessing: false,
    isLoading: true,
    error: null,
    imageDimensions: null,
    imageWidth: 0,
    imageHeight: 0,
    videoDuration: null,
    showDetections: true,
    async init() {
      try {
        const storedFile = await getCurrentUpload();

        if (!storedFile) {
          this.error = "No file found.";
          this.isLoading = false;

          Alpine.store("notifications").warning(
            "Your uploaded file could not be found. Please select it again.",
          );

          window.location.replace("/detect");
          return;
        }

        this.file = storedFile.file;
        this.detections = storedFile.detections || null;
        await this.setPreview(this.file);

        if (this.fileType === "image") await this.generateDetectionCrops();
        if (this.fileType === "video") await this.generateVideoDetectionCrops();
        if (this.fileType === "document")
          await this.generateDocumentDetectionCrops();
      } catch (error) {
        this.error = notifyError(error, "Failed to load the results.");
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
            this.error = notifyError(
              error,
              "Failed to generate image preview.",
            );
          }
        }
      } else if (videoFormats.includes(extension)) {
        this.fileType = "video";
        this.previewUrl = URL.createObjectURL(file);
      } else if (documentFormats.includes(extension)) {
        this.fileType = "document";

        try {
          const preview = await fetchPreview(file, "document");
          this.previewUrl = preview.url;
        } catch (error) {
          this.error = notifyError(
            error,
            "Failed to generate document preview.",
          );
        }
      } else if (file.type.startsWith("image/")) {
        this.fileType = "image";

        try {
          const preview = await fetchPreview(file, "image");
          this.previewUrl = preview.url;
        } catch (error) {
          this.error = notifyError(error, "Failed to generate image preview.");
        }
      } else {
        this.fileType = "document";

        try {
          const preview = await fetchPreview(file, "document");
          this.previewUrl = preview.url;
        } catch (error) {
          this.error = notifyError(
            error,
            "Failed to generate document preview.",
          );
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
      if (seconds == null || !Number.isFinite(seconds)) return "";

      const totalSeconds = Math.floor(seconds);
      const minutes = Math.floor(totalSeconds / 60);
      const remainingSeconds = totalSeconds % 60;
      return `${String(minutes).padStart(2, "0")}:${String(
        remainingSeconds,
      ).padStart(2, "0")}`;
    },
    handleImageLoad(event) {
      const image = event.target;

      this.imageWidth = image.naturalWidth;
      this.imageHeight = image.naturalHeight;
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
        this.error = notifyError(error, "Failed to replace the file.");
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
    detectionName(detection) {
      if (detection.text) return detection.text;

      const target = detection.target || detection.type;
      const names = {
        faces: "Face",
        plates: "License Plate",
        text: "Text",
        pii: "Personal Information",
      };

      const name = names[target] || "Detection";
      const detectionId = detection.uniqueId || detection.id;
      const detections = this.detectionsFor(target);
      const index = detections.findIndex(
        (item) => (item.uniqueId || item.id) === detectionId,
      );

      return index >= 0 ? `${name} ${index + 1}` : name;
    },
    detectionTargetLabel(detection) {
      const target = detection.target || detection.type;
      const names = {
        faces: "Face",
        plates: "Plate",
        text: "Text",
        pii: "PII",
      };

      return names[target] || "Detection";
    },
    confidenceLabel(confidence) {
      if (confidence == null) return "";

      const percentage = `${(confidence * 100).toFixed(1)}%`;
      if (confidence >= 0.8) return `${percentage} confidence · High`;
      if (confidence >= 0.5) return `${percentage} confidence · Medium`;

      return `${percentage} confidence · Low`;
    },
    confidenceClass(confidence) {
      if (confidence >= 0.8) return "text-emerald-400";
      if (confidence >= 0.5) return "text-amber-400";

      return "text-red-400";
    },
    detectionGroups() {
      const empty = {
        faces: [],
        plates: [],
        text: [],
        pii: [],
      };

      if (!this.detections) return empty;
      if (!Array.isArray(this.detections))
        return {
          faces: (this.detections.faces || []).map((detection) => ({
            ...detection,
            target: "faces",
          })),
          plates: (this.detections.plates || []).map((detection) => ({
            ...detection,
            target: "plates",
          })),
          text: (this.detections.text || []).map((detection) => ({
            ...detection,
            target: "text",
          })),
          pii: (this.detections.pii || []).map((detection) => ({
            ...detection,
            target: "pii",
          })),
        };

      const grouped = {
        faces: [],
        plates: [],
        text: [],
        pii: [],
      };

      for (const result of this.detections) {
        if (!result) continue;
        if (result.page != null) {
          const page = result.page;
          for (const target of ["faces", "plates", "text", "pii"]) {
            const detections = result[target] || [];
            for (const detection of detections)
              grouped[target].push({
                ...detection,
                target,
                page,
                uniqueId: detection.id,
              });
          }

          continue;
        }

        if (result.frame != null) {
          const frame = result.frame;
          for (const target of ["faces", "plates", "text", "pii"]) {
            const detections = result.detections?.[target] || [];
            for (const detection of detections) {
              const existing = grouped[target].find(
                (item) => item.uniqueId === detection.id,
              );
              if (existing) continue;

              grouped[target].push({
                ...detection,
                target,
                frame,
                timestamp: result.timestamp,
                uniqueId: detection.id,
              });
            }
          }
        }
      }

      return grouped;
    },
    detectionsFor(target) {
      return this.detectionGroups()[target] || [];
    },
    totalDetectionCount() {
      const groups = this.detectionGroups();
      return (
        groups.faces.length +
        groups.plates.length +
        groups.text.length +
        groups.pii.length
      );
    },
    selectedVideoDetections() {
      const selectedIds = new Set(
        this.selectedDetections.map(
          (detection) =>
            `${detection.target}:${detection.uniqueId || detection.id}`,
        ),
      );

      const selected = [];
      for (const result of this.detections || []) {
        if (!result || result.frame == null) continue;
        const frame = Number(result.frame);
        for (const target of ["faces", "plates", "text", "pii"]) {
          const detections = result.detections?.[target] || [];
          for (const detection of detections) {
            const id = detection.id;
            if (!id) continue;

            const key = `${target}:${id}`;
            if (!selectedIds.has(key)) continue;

            selected.push({
              ...detection,
              target,
              frame,
              timestamp: result.timestamp,
            });
          }
        }
      }

      return selected;
    },
    isDetectionSelected(detection) {
      return this.selectedDetections.some((item) => item.id === detection.id);
    },
    toggleDetection(detection) {
      const index = this.selectedDetections.findIndex(
        (item) => item.id === detection.id,
      );

      if (index === -1) this.selectedDetections.push(detection);
      else this.selectedDetections.splice(index, 1);
    },
    allDetections() {
      const groups = this.detectionGroups();
      return [...groups.faces, ...groups.plates, ...groups.text, ...groups.pii];
    },
    allDetectionsSelected() {
      const all = this.allDetections();
      return (
        all.length > 0 &&
        all.every((detection) => this.isDetectionSelected(detection))
      );
    },
    toggleSelectAll() {
      if (this.allDetectionsSelected()) {
        this.selectedDetections = [];
        return;
      }

      this.selectedDetections = [...this.allDetections()];
    },
    formatDetectionTimeRange(detection) {
      const start = this.formatDuration(detection.start_time);
      const end = this.formatDuration(detection.end_time);

      let result = `${start} → ${end}`;
      if (detection.frame_count != null)
        result += ` (${detection.frame_count} frames)`;

      return result;
    },
    isCropDetection(detection) {
      const target = detection.target;
      return target === "faces" || target === "plates";
    },
    async generateDetectionCrops() {
      if (this.fileType !== "image" || !this.previewUrl) return;

      const detections = [
        ...this.detectionsFor("faces"),
        ...this.detectionsFor("plates"),
      ];

      if (!detections.length) return;
      const image = new Image();

      await new Promise((resolve, reject) => {
        image.onload = resolve;
        image.onerror = reject;
        image.src = this.previewUrl;
      });

      for (const detection of detections) {
        const key = detection.uniqueId || detection.id;
        try {
          const cropUrl = await this.createDetectionCrop(image, detection);
          if (cropUrl) this.cropUrls[key] = cropUrl;
        } catch (error) {
          console.error("Failed to create crop:", detection, error);
        }
      }
    },
    async loadDocumentPage(page) {
      const response = await fetch(
        `${API_BASE}/documents/page-preview?page=${encodeURIComponent(page)}`,
        {
          method: "POST",
          body: (() => {
            const formData = new FormData();
            formData.append("file", this.file);
            return formData;
          })(),
        },
      );

      if (!response.ok) {
        let message = `Failed to load page ${page}.`;

        try {
          const data = await response.json();
          message = data.error || message;
        } catch {}

        throw new Error(message);
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const image = new Image();

      await new Promise((resolve, reject) => {
        image.onload = resolve;
        image.onerror = reject;
        image.src = url;
      });

      image._objectUrl = url;

      return image;
    },
    async generateDocumentDetectionCrops() {
      if (this.fileType !== "document") return;

      const detections = [
        ...this.detectionsFor("faces"),
        ...this.detectionsFor("plates"),
      ];

      if (!detections.length) return;
      const pages = [
        ...new Set(
          detections
            .map((detection) => detection.page)
            .filter((page) => page != null),
        ),
      ];

      for (const page of pages) {
        try {
          const pageImage = await this.loadDocumentPage(page);
          if (!pageImage) continue;

          this.documentPages[page] = pageImage;
        } catch (error) {
          notifyError(error, `Failed to load document page ${page}.`);
        }
      }

      for (const detection of detections) {
        const key = detection.uniqueId || detection.id;
        const pageImage = this.documentPages[detection.page];
        if (!pageImage) continue;

        try {
          const cropUrl = await this.createDetectionCrop(pageImage, detection);
          if (cropUrl) this.cropUrls[key] = cropUrl;
        } catch (error) {
          console.error("Failed to create document crop:", detection, error);
        }
      }
    },
    createDetectionCrop(media, detection) {
      return new Promise((resolve) => {
        const mediaWidth = media.naturalWidth ?? media.videoWidth;
        const mediaHeight = media.naturalHeight ?? media.videoHeight;

        if (!mediaWidth || !mediaHeight) {
          resolve(null);
          return;
        }

        let x1 = Number(detection.x1);
        let y1 = Number(detection.y1);
        let x2 = Number(detection.x2);
        let y2 = Number(detection.y2);

        if (
          !Number.isFinite(x1) ||
          !Number.isFinite(y1) ||
          !Number.isFinite(x2) ||
          !Number.isFinite(y2)
        ) {
          resolve(null);
          return;
        }

        const boxWidth = x2 - x1;
        const boxHeight = y2 - y1;

        if (boxWidth <= 0 || boxHeight <= 0) {
          resolve(null);
          return;
        }

        const padding = 0.6;
        x1 -= boxWidth * padding;
        y1 -= boxHeight * padding;
        x2 += boxWidth * padding;
        y2 += boxHeight * padding;

        let cropWidth = x2 - x1;
        let cropHeight = y2 - y1;

        const centerX = (x1 + x2) / 2;
        const centerY = (y1 + y2) / 2;

        const cropSize = Math.max(cropWidth, cropHeight);
        x1 = centerX - cropSize / 2;
        x2 = centerX + cropSize / 2;
        y1 = centerY - cropSize / 2;
        y2 = centerY + cropSize / 2;

        if (x1 < 0) {
          x2 -= x1;
          x1 = 0;
        }

        if (y1 < 0) {
          y2 -= y1;
          y1 = 0;
        }

        if (x2 > mediaWidth) {
          const overflow = x2 - mediaWidth;
          x1 -= overflow;
          x2 = mediaWidth;
        }

        if (y2 > mediaHeight) {
          const overflow = y2 - mediaHeight;
          y1 -= overflow;
          y2 = mediaHeight;
        }

        x1 = Math.max(0, x1);
        y1 = Math.max(0, y1);
        x2 = Math.min(mediaWidth, x2);
        y2 = Math.min(mediaHeight, y2);

        cropWidth = x2 - x1;
        cropHeight = y2 - y1;

        if (cropWidth <= 0 || cropHeight <= 0) {
          resolve(null);
          return;
        }

        const canvas = document.createElement("canvas");
        canvas.width = Math.round(cropWidth);
        canvas.height = Math.round(cropHeight);

        const context = canvas.getContext("2d");
        if (!context) {
          resolve(null);
          return;
        }

        context.drawImage(
          media,
          x1,
          y1,
          cropWidth,
          cropHeight,
          0,
          0,
          canvas.width,
          canvas.height,
        );

        resolve(canvas.toDataURL("image/jpeg", 0.9));
      });
    },
    async generateVideoDetectionCrops() {
      if (this.fileType !== "video" || !this.previewUrl) return;

      const detections = [
        ...this.detectionsFor("faces"),
        ...this.detectionsFor("plates"),
      ];
      if (!detections.length) return;

      const video = document.createElement("video");
      video.preload = "metadata";
      video.muted = true;
      video.playsInline = true;
      video.src = this.previewUrl;

      await new Promise((resolve, reject) => {
        video.onloadedmetadata = resolve;
        video.onerror = reject;
      });

      for (const detection of detections) {
        const key = detection.uniqueId || detection.id;
        try {
          const cropUrl = await this.createVideoDetectionCrop(video, detection);
          if (cropUrl) this.cropUrls[key] = cropUrl;
        } catch (error) {
          console.error(
            "Failed to create video detection crop:",
            detection,
            error,
          );
        }
      }
    },
    async createVideoDetectionCrop(video, detection) {
      if (detection.timestamp == null) {
        console.warn("Video detection has no timestamp:", detection);
        return null;
      }

      await this.seekVideo(video, detection.timestamp);
      return this.createDetectionCrop(video, detection);
    },
    seekVideo(video, time) {
      return new Promise((resolve, reject) => {
        const handleSeeked = () => {
          cleanup();
          resolve();
        };

        const handleError = () => {
          cleanup();
          reject(new Error("Failed to seek video"));
        };

        const cleanup = () => {
          video.removeEventListener("seeked", handleSeeked);
          video.removeEventListener("error", handleError);
        };

        video.addEventListener("seeked", handleSeeked);
        video.addEventListener("error", handleError);
        video.currentTime = Math.min(Math.max(0, time), video.duration);
      });
    },
    async anonymizeSelected() {
      if (this.selectedDetections.length === 0) {
        Alpine.store("notifications").warning(
          "Select at least one detection to anonymize.",
        );
        return;
      }

      this.isProcessing = true;
      try {
        let endpoint;
        if (this.fileType === "image")
          endpoint = `${API_BASE}/images/anonymize-selected`;
        else if (this.fileType === "video")
          endpoint = `${API_BASE}/videos/anonymize-selected`;
        else if (this.fileType === "document")
          endpoint = `${API_BASE}/documents/anonymize-selected`;
        else throw new Error("Unsupported file type.");

        const formData = new FormData();
        formData.append("file", this.file);

        const detectionsToSend =
          this.fileType === "video"
            ? this.selectedVideoDetections()
            : this.selectedDetections;

        formData.append("detections", JSON.stringify(detectionsToSend));

        const params = new URLSearchParams();
        params.set("mode", this.mode);
        params.set("padding", String(this.padding / 100));

        const response = await fetch(`${endpoint}?${params.toString()}`, {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          let message = `Anonymization failed with status ${response.status}.`;
          try {
            const data = await response.json();
            message = data.error || message;
          } catch {}

          throw new Error(message);
        }

        const blob = await response.blob();
        const filename = this.getOutputFilename();
        await storeProcessedFile(blob, filename);

        window.location.href = "/complete";
      } catch (error) {
        notifyError(error, "Failed to anonymize the file.");
      } finally {
        this.isProcessing = false;
      }
    },
    getOutputFilename() {
      if (!this.file) return "anonymized";
      const extension = this.getExtension(this.file);

      return `${this.file.name.replace(/\.[^/.]+$/, "")}-anonymized.${extension}`;
    },
    destroy() {
      if (this.previewUrl) URL.revokeObjectURL(this.previewUrl);
    },
    isDocument() {
      return this.fileType === "document" || this.fileType === "pdf";
    },
  };
}

function completePage() {
  return {
    originalUrl: null,
    processedUrl: null,
    fileName: "Anonymized file",
    outputName: "anonymized",
    mediaType: "image",
    position: 50,
    dragging: false,
    isLoading: true,
    error: null,
    isDownloading: false,

    async init() {
      try {
        const storedFile = await getCurrentUpload();
        if (!storedFile) {
          this.error = "No file found.";
          this.isLoading = false;
          Alpine.store("notifications").warning(
            "Your anonymized file could not be found. Please select it again.",
          );

          window.location.replace("/detect");
          return;
        }

        if (!storedFile.processedFile) {
          this.error = "No processed file found.";
          this.isLoading = false;
          Alpine.store("notifications").warning(
            "Your anonymized file could not be found. Please process the file again.",
          );

          window.location.replace("/results");
          return;
        }

        this.fileName = storedFile.file.name;
        this.outputName = storedFile.outputName;
        this.mediaType = this.getMediaType(storedFile.file);
        if (this.mediaType === "image") {
          this.originalUrl = await this.getImagePreview(storedFile.file);
          const processedFile = new File(
            [storedFile.processedFile],
            storedFile.outputName,
            {
              type: storedFile.processedFile.type,
            },
          );

          this.processedUrl = await this.getImagePreview(processedFile);
        } else {
          this.originalUrl = URL.createObjectURL(storedFile.file);
          this.processedUrl = URL.createObjectURL(storedFile.processedFile);
        }

        this.isLoading = false;
      } catch (error) {
        this.error = notifyError(error, "Failed to load the anonymized file.");
        this.isLoading = false;
      }
    },
    async getImagePreview(file) {
      const extension = this.getExtension(file);
      const browserPreviewableImages = ["jpg", "jpeg", "png", "webp", "gif"];
      if (browserPreviewableImages.includes(extension))
        return URL.createObjectURL(file);

      const preview = await fetchPreview(file, "image");
      return preview.url;
    },
    getExtension(file) {
      if (!file?.name) return "";
      return file.name.split(".").pop().toLowerCase();
    },
    getMediaType(file) {
      const extension = this.getExtension(file);
      const imageFormats = [
        "jpg",
        "jpeg",
        "png",
        "webp",
        "gif",
        "tif",
        "tiff",
        "heic",
        "heif",
      ];

      const videoFormats = ["mp4", "mov", "avi", "mkv", "webm"];
      if (imageFormats.includes(extension)) return "image";
      if (videoFormats.includes(extension)) return "video";
      if (file.type.startsWith("image/")) return "image";
      if (file.type.startsWith("video/")) return "video";

      return "document";
    },
    move(event) {
      if (!this.dragging || !this.$refs.wrapper) return;

      const rect = this.$refs.wrapper.getBoundingClientRect();
      this.position = Math.min(
        100,
        Math.max(0, ((event.clientX - rect.left) / rect.width) * 100),
      );
    },
    download() {
      if (!this.processedUrl || this.isDownloading) return;

      this.isDownloading = true;

      const link = document.createElement("a");
      link.href = this.processedUrl;
      link.download = this.outputName;

      document.body.appendChild(link);
      link.click();
      link.remove();

      Alpine.store("notifications").success(
        "Your anonymized file has been downloaded.",
      );

      setTimeout(() => {
        this.isDownloading = false;
      }, 2500);
    },
    processAnother() {
      sessionStorage.removeItem("originalUrl");
      sessionStorage.removeItem("processedUrl");
      sessionStorage.removeItem("fileName");
      sessionStorage.removeItem("outputName");
      sessionStorage.removeItem("mediaType");

      window.location.href = "/detect";
    },
  };
}
