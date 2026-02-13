from app.ingestion.pdf_loader import chunk_text


def test_chunk_text_basic():
    text = "\n\n".join(["Paragraph %d" % i for i in range(10)])
    chunks = chunk_text(text, chunk_size=50, overlap=10)
    assert len(chunks) >= 1
    for c in chunks:
        assert isinstance(c, str)
