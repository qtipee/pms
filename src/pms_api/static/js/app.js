
document.addEventListener('DOMContentLoaded', (evt) => {
    // Elements with class « file-field »
    document.querySelectorAll('.file-field').forEach((item, i) => {
        // Drag enter -> modify style
        item.addEventListener('dragenter', evt => {
            evt.preventDefault()
            item.classList.add('dragenter')
        })

        // Drag leave -> modify style
        item.addEventListener('dragleave', evt => {
            evt.preventDefault()
            item.classList.remove('dragenter')
        })

        // Drop on « file input »
        item.addEventListener('drop', evt => {
            evt.preventDefault()

            let input = item.querySelector('.dand-file-input')
            let files = evt.dataTransfer.files
            parseAudioFiles(input, files)
        });
    });

    // Elements with class « dand-file-input »
    document.querySelectorAll('.dand-file-input').forEach((item, i) => {
        // File uploaded by file dialog
        item.addEventListener('change', (evt) => {
            evt.preventDefault()

            let files = evt.target.files
            parseAudioFiles(item, files)
        })
    })

    // Elements with class « close »
    document.querySelectorAll('.close').forEach((item, i) => {
        let input = item.parentElement.parentElement.parentElement.querySelector('.dand-file-input')

        // Drag & Drop « close » icon
        item.addEventListener('click', evt => {
            showDragDropFigure(input)
        })
    })
})

function parseAudioFiles(input, files) {
    if (files.length > 1) {
        alert('You can only upload one audio file at a time.');
    }
    else {
        let file = files[0];
        let fileName = file.name;
        let fileType = file.type;
        let fileSize = file.size;

        // Must be audio file
        if (! fileType.includes('image')) {
            alert('The file must be an image.');
        }
        // Size cannot exceed 50 MB
        else if (fileSize > 5e7) {
            alert('The file size cannot exceed 50 MB.')
        }
        // All right
        else {
            input.files = files;
            showUploadedFile(input);
        }
    }
}

const $$ = {
    dragDropFigure: document.querySelector('.dragdrop-figure'),
    dragDropUploaded: document.querySelector('.dragdrop-uploaded'),
    dragDropCloses: document.querySelectorAll('.dragdrop-uploaded .close'),
}

function showUploadedFile(input) {
    // Displays the uploaded sound file information
    let file = input.files[0];
    $$.dragDropUploaded.querySelector('.uploaded-file-name').innerHTML = file.name;
    $$.dragDropUploaded.querySelector('.uploaded-file-size').innerHTML = parseSize(file.size);

    $$.dragDropFigure.setAttribute('hidden', true);
    $$.dragDropUploaded.removeAttribute('hidden');
}

function showDragDropFigure(input) {
    // Displays the Drag & Drop information
    input.value = '';

    $$.dragDropUploaded.setAttribute('hidden', true);
    $$.dragDropFigure.removeAttribute('hidden');
}

function parseSize(bytes) {
    let sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];

    if (bytes == 0) { return '0 Byte' }

    let i = Math.floor(Math.log(bytes) / Math.log(1000))

    return (bytes / Math.pow(1000, i)).toFixed(2) + ' ' + sizes[i]
}
