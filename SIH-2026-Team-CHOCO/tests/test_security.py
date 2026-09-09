"""Unit tests for IPFS encryption, file validation, LLM safe-query guards."""


from api.services.ipfs import decrypt_file, encrypt_file, sha256_file, validate_file
from api.services.llm_agent import validate_query


def test_encrypt_decrypt_roundtrip():
    data = b"top-secret-evidence-bytes" * 100
    blob = encrypt_file(data)
    assert blob != data
    assert decrypt_file(blob) == data


def test_encryption_produces_unique_blobs():
    data = b"same input"
    assert encrypt_file(data) != encrypt_file(data)  # random nonce


def test_sha256_file():
    h = sha256_file(b"abc")
    assert len(h) == 64
    assert sha256_file(b"abc") == h


def test_file_validation_ok():
    err = validate_file("photo.jpg", b"\xff\xd8\xff" + b"\x00" * 100)
    assert err is None


def test_file_validation_rejects_bad_magic():
    err = validate_file("photo.jpg", b"\x89PNG" + b"\x00" * 100)
    assert err is not None


def test_file_validation_rejects_extension():
    err = validate_file("virus.exe", b"MZ" + b"\x00" * 100)
    assert "not allowed" in err


def test_file_validation_rejects_oversize():
    err = validate_file("big.pdf", b"%PDF-" + b"\x00" * (10 * 1024 * 1024 + 1))
    assert "10MB" in err


# --- LLM safe Cypher validation ---

def test_safe_query_passes():
    assert validate_query("MATCH (a:Account {account_id: $id}) RETURN a LIMIT 10") is None


def test_create_blocked():
    assert validate_query("CREATE (a:Account)") is not None


def test_delete_blocked():
    assert validate_query("MATCH (a) DELETE a") is not None


def test_merge_blocked():
    assert validate_query("MATCH (a) MERGE (a)-[:X]->(b)") is not None


def test_semicolon_blocked():
    assert validate_query("MATCH (a) RETURN a; DROP DATABASE") is not None


def test_non_read_start_blocked():
    assert validate_query("SET a.x = 1") is not None
