const express = require("express");
const multer = require("multer");
const upload = multer({ dest: "uploads/" });
const app = express();
app.use(express.json());

app.post("/upload_files", upload.array("files"), uploadFiles);
app.get("/", function(req,res){
    console.log("Working");
})

function uploadFiles(req, res) {
    console.log(req.body);
    console.log(req.files);
    res.json({ message: "Successfully uploaded files" });
}
app.listen(7000, () => {
    console.log(`Server started...`);
});