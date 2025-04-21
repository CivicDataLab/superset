import asyncio
import re

import polib
from googletrans import Translator


async def main():

    def mask_placeholders(text):
        """Replace %(...)s with __PH0__, __PH1__, ... and keep mapping"""
        placeholders = re.findall(r'%\([^)]+\)s', text)
        masked = text
        mapping = {}

        for i, ph in enumerate(placeholders):
            token = f"__PH{i}__"
            masked = masked.replace(ph, token)
            mapping[token] = ph

        return masked, mapping

    def unmask_placeholders(text, mapping):
        """Replace __PH0__, etc. back with original placeholders"""
        for token, original in mapping.items():
            text = text.replace(token, original)
        return text

    # Translate from english to thai
    po = polib.pofile("superset/translations/th/LC_MESSAGES/messages.po")
    translator = Translator()
    print("File located. Starting translation...")
    for entry in po.untranslated_entries():
        if entry.msgid.strip():
            try:
                masked_msgid, ph_map = mask_placeholders(entry.msgid)
                translated = await translator.translate(
                    masked_msgid, src="en", dest="th")
                entry.msgstr = unmask_placeholders(translated.text, ph_map)

                # translated = await translator.translate(entry.msgid, src="en", dest="th")
                # entry.msgstr = preserve_placeholders(
                #     entry.msgid, translated.text)
                print(f"Translated '{entry.msgid}'")
            except Exception as e:
                print(f"Error translating '{entry.msgid}': {e}")

    po.save("superset/translations/th/LC_MESSAGES/messages.po")

# Run the async main
asyncio.run(main())
