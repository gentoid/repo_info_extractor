from pprint import pprint
import pathlib
import os
import hashlib as md5

supported_library_languages = {
    'JavaScript': ['js', 'jsx'],
    'Python': ['py'],
    'Markdown': ['md'],
}

class AnalyzeLibraries:
    def __init__(self, commit_list, authors, basedir, skip_obfuscation):
        self.commit_list = commit_list
        self.authors = authors
        self.basedir = basedir
        self.skip_obfuscation = skip_obfuscation

    # Return a dict of commit -> language -> list of libraries
    def get_libraries(self):
        processed_authors = []
        if not self.skip_obfuscation:
            for email, name in self.authors:
                # This logic is in two places now...
                # Do we need to check for empty email?
                # This logic is duplicated, same as in commits.py. Move to obfuscator
                name_md5_hash = md5.md5()
                name_md5_hash.update(name.encode('utf-8'))
                email_md5_hash = md5.md5()
                email_md5_hash.update(email.encode('utf-8'))
                processed_authors.append({name_md5_hash.hexdigest(), email_md5_hash.hexdigest()})
        else:
            processed_authors = self.authors
 
        commits = filter_commits_by_authors(self.commit_list, processed_authors)
        for commit in commits:
            files = [os.path.join(self.basedir, x.file_name) for x in commit.changed_files]
            for lang, extensions in supported_library_languages.items():
                # we have extensions now, filter the list to only files with those extensions
                lang_files = list(filter(lambda x: pathlib.Path(x).suffix[1:] in extensions, files))
                if lang_files:
                    # if we go to this point, there were files modified in the language we support
                    # now we need to run regex for imports for every single of such file
                    print(lang_files)
    
        return []

# Return only commits authored by provided obfuscated_author_emails
def filter_commits_by_authors(commit_list, authors):
    return list(filter(lambda x: {x.author_name, x.author_email} in authors, commit_list))
