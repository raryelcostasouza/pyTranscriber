from whisper.tokenizer import get_tokenizer, Tokenizer, LANGUAGES

class CustomTokenizer(Tokenizer):
    def __init__(self):
        tokenizer = get_tokenizer(multilingual=True)

        # Copy base tokenizer attributes
        self.__dict__.update(tokenizer.__dict__)

    def __post_init__(self):
        # Build the special token mapping
        for special in self.encoding.special_tokens_set:
            special_token = self.encoding.encode_single_token(special)
            self.special_tokens[special] = special_token

        # Get the required special tokens
        sot: int = self.special_tokens["<|startoftranscript|>"]
        translate: int = self.special_tokens["<|translate|>"]
        transcribe: int = self.special_tokens["<|transcribe|>"]

        langs = tuple(LANGUAGES.keys())

        # Create start of transcript sequence
        sot_sequence = [sot]
        if self.language is not None:
            if self.language not in langs:
                raise ValueError(f"Language '{self.language}' not supported in custom tokenizer.")
            sot_sequence.append(sot + 1 + langs.index(self.language))
        if self.task is not None:
            task_token: int = transcribe if self.task == "transcribe" else translate
            sot_sequence.append(task_token)

        self.sot_sequence = tuple(sot_sequence)
    def encode(self, text: str):
        return super().encode(text)

    def decode(self, tokens):
        return super().decode(tokens)