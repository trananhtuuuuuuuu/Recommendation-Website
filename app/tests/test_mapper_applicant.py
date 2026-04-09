from app.mappers.mapper_applicant import MapperApplicant


def test_hash_password():
    # Ensure hashing returns different string than input and is deterministic-ish
    plain = "MyS3cret!"
    hashed = MapperApplicant.hash_password(plain)
    assert hashed != plain
    # When using fallback (sha256) the hash should be hex of length 64
    if len(hashed) == 64:
        import hashlib
        assert hashed == hashlib.sha256(plain.encode("utf-8")).hexdigest()
