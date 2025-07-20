# adobe-hackathon


## Challenge 1a

### Build Command
```bash + powershell
    docker build --platform linux/amd64 -t pdf-outline-extractor .
```

### Run Command:
```bash
    docker run --rm -v $(pwd)/input:/app/input:ro -v $(pwd)/output/:/app/output --network none pdf-outline-extractor
```

### Run command:
```powershell
    docker run --rm -v ${PWD}/input:/app/input:ro -v ${PWD}/output/:/app/output --network none pdf-outline-extractor
```