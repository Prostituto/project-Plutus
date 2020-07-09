a = """{"code":"invalid_credentials","message":"You entered the wrong credentials. Please check that the login/password is correct."}"""
b = "{"\
    "\"code\":\"invalid_credentials\","\
    "\"message\":\"You entered the wrong credentials. Please check that the login/password is correct.\""\
"}"

print(a)
print(b)

print(a == b)
