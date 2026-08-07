function filePreview() {
  return {
    file: null,
    previewUrl: null,
    fileType: null,
    previewType: null,
    isDragging: false,
    async init() {
      const storedFile = await getUploadedFile();

      if (storedFile) {
        this.setFile(storedFile);
        await deleteUploadedFile();
      }
    },
    handleFile(event) {
      const file = event.target.files?.[0];

      if (!file) return;
      this.setFile(file);

      event.target.value = "";
    },
    handleDrop(event) {
      this.isDragging = false;

      const file = event.dataTransfer.files?.[0];
      if (!file) return;

      this.setFile(file);
    },
    setFile(file) {
      this.file = file;

      if (this.previewUrl) URL.revokeObjectURL(this.previewUrl);
      this.previewUrl = URL.createObjectURL(file);

      const extension = this.getExtension(file);
      const previewableImages = ["jpg", "jpeg", "png", "webp", "gif"];
      const videoFormats = ["mp4", "mov", "avi", "mkv", "webm"];
      const imageFormats = [
        "jpg",
        "jpeg",
        "png",
        "webp",
        "tif",
        "tiff",
        "heic",
        "heif",
        "gif",
      ];

      if (previewableImages.includes(extension)) {
        this.fileType = "image";
        this.previewType = "image";
      } else if (videoFormats.includes(extension)) {
        this.fileType = "video";
        this.previewType = "video";
      } else if (imageFormats.includes(extension)) {
        this.fileType = "image";
        this.previewType = "file";
      } else {
        this.fileType = "document";
        this.previewType = "file";
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

async function getUploadedFile() {
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

      resolve(entry.file);
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
        window.location.href = "/anonymize";
      } catch (error) {
        console.error("Failed to store file:", error);
      }
    },
  };
}
