```                  
                              Any Source
                                      ↓
                            Detect File Type
                                      ↓
       ┌────────────┼────────────┐
       ↓                             ↓                             ↓
      PDF                       TXT                    DOCX/HTML
       ↓                              ↓                            ↓
PyMuPDF4LLM        TextLoader               Docling
       └────────────┼────────────┘
                                      ↓
                               Document[]
                                      ↓
                            Medical Chunking
                                      ↓
                                Vector DB
```