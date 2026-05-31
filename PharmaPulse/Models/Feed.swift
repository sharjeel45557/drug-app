import Foundation

/// Top-level document the app downloads from GitHub Pages (docs/feed.json).
/// The schema intentionally mirrors the original PharmaPulse HTML `DATA` objects
/// so the weekly Citeline pipeline can keep producing the same shape.
struct Feed: Codable, Equatable {
    let schemaVersion: Int
    let generatedAt: String
    let weekRange: String
    let source: String
    let articles: [Article]

    /// `generatedAt` parsed as a Date (ISO-8601), if possible.
    var generatedDate: Date? {
        ISO8601DateFormatter().date(from: generatedAt)
    }
}

/// A single pharma-news item with its impact analysis.
struct Article: Codable, Identifiable, Hashable {
    let id: Int
    let category: String
    let catClass: String
    let borderClass: String
    let headline: String
    let details: String
    let drugs: String
    let impact: String
    let url: String
    let date: String?

    var sourceURL: URL? { URL(string: url) }

    /// `date` ("yyyy-MM-dd") parsed to a Date for display/sorting.
    var publishedDate: Date? {
        guard let date else { return nil }
        let f = DateFormatter()
        f.locale = Locale(identifier: "en_US_POSIX")
        f.dateFormat = "yyyy-MM-dd"
        return f.date(from: date)
    }
}
