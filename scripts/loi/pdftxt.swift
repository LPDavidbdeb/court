// Extrait la couche texte d'un PDF via PDFKit.
// Les PDF de LegisQuébec n'ont pas de couche image : PDFKit suffit.
// Raison d'être : ni fitz (PyMuPDF) ni pypdf ne sont installables sur cette machine.
import Foundation
import PDFKit

let args = CommandLine.arguments
guard args.count > 1 else {
    FileHandle.standardError.write("usage: pdftxt <fichier.pdf>\n".data(using: .utf8)!)
    exit(2)
}
guard let doc = PDFDocument(url: URL(fileURLWithPath: args[1])) else {
    FileHandle.standardError.write("PDF illisible : \(args[1])\n".data(using: .utf8)!)
    exit(1)
}
print(doc.string ?? "")
