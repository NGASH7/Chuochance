$('#modal').on('shown.bs.modal', function () {
	const recommendation_url = $("#school_recommendation").val();
	const father_url = $("#death_cert_father").val();
	const mother_url = $("#death_cert_mother").val();

	const load_pdf = function (canvas_id, url, prevID, nextID, pageID) {
		var pdfScale = 2.0;
		(async function () {

			// Specified the workerSrc property
			pdfjsLib.GlobalWorkerOptions.workerSrc = "https://cdn.jsdelivr.net/npm/pdfjs-dist@2.7.570/build/pdf.worker.js";

			// Create the PDF document
			const doc = await pdfjsLib.getDocument(url).promise;

			const minPage = 1;
			const maxPage = doc._pdfInfo.numPages;
			let currentPage = 1;

			// Get page 1
			await getPage(doc, currentPage);

			// Display the page number
			document.getElementById(pageID).innerHTML = `Page ${currentPage} of ${maxPage}`;

			// The previous button click event
			document.getElementById(prevID).addEventListener("click", async () => {

				if (currentPage > minPage) {

					// Get the previous page
					await getPage(doc, currentPage--);

					// Display the page number
					document.getElementById(pageID).innerHTML = `Page ${currentPage} of ${maxPage}`;

				}

			});

			// The next button click event
			document.getElementById(nextID).addEventListener("click", async () => {

				if (currentPage < maxPage) {

					// Get the next page
					await getPage(doc, currentPage++);

					// Display the page number
					document.getElementById(pageID).innerHTML = `Page ${currentPage} of ${maxPage}`;

				}

			});

			// The zoom in button click event
			// document.getElementById(zoomID).addEventListener("click", async () => {
			// 	pdfScale = pdfScale + 0.25;
			// 	await getPage(doc, currentPage);
			// });

		})();
		async function getPage(doc, pageNumber) {

			if (pageNumber >= 1 && pageNumber <= doc._pdfInfo.numPages) {

				// Fetch the page
				const page = await doc.getPage(pageNumber);

				// Set the viewport
				var scale = pdfScale;
				const viewport = page.getViewport({ scale: scale });

				// Set the canvas dimensions to the PDF page dimensions
				const canvas = document.getElementById(canvas_id);
				const context = canvas.getContext("2d");
				canvas.height = viewport.height;
				canvas.width = viewport.width;

				// Render the PDF page into the canvas context
				return await page.render({
					canvasContext: context,
					viewport: viewport
				}).promise;

			} else {
				console.log("Please specify a valid page number");
			}

		}
	}

	if (recommendation_url) {
		load_pdf("school_canvas", recommendation_url, 'previous_school', 'next_school', 'school_pageNumber');
	}
	if (father_url) {
		load_pdf("father_canvas", father_url, 'previous_father', 'next_father', 'father_pageNumber');
	}
	if (mother_url) {
		load_pdf("mother_canvas", mother_url, 'previous_mother', 'next_mother', 'mother_pageNumber');
	}
});

$(function () {
	$('input[type="text"]').keyup(function () {
		this.value = this.value.toUpperCase();
	});
	$('input[type="email"]').keyup(function () {
		this.value = this.value.toLowerCase();
	});
});
$(".dateinput").datetimepicker({
	format: 'Y-m-d',
	timepicker: false,
});
$(".datetimeinput").datetimepicker({
	format: 'Y-m-d H:i:s',
});

$(".phone_input").each(function () {
	$(this).intlTelInput({
		initialCountry: "KE",
		customPlaceholder: "700111222 or 100111222",
		separateDialCode: true,
	});
});