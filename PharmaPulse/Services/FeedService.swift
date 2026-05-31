import Foundation

/// Loads the news feed with a three-tier strategy:
///   1. show cached/bundled data instantly,
///   2. fetch the latest feed.json from GitHub Pages,
///   3. persist the newest copy to disk for offline use.
///
/// Update the `feedURL` once GitHub Pages is enabled for the repo.
@MainActor
final class FeedStore: ObservableObject {

    // MARK: Published state
    @Published private(set) var articles: [Article] = []
    @Published private(set) var weekRange: String = ""
    @Published private(set) var lastUpdated: Date?
    @Published private(set) var isLoading = false
    @Published private(set) var errorMessage: String?

    // MARK: Configuration
    /// Where the weekly pipeline publishes the feed.
    /// GitHub Pages project URL for `sharjeel45557/drug-app` serving the /docs folder.
    private let feedURL = URL(string: "https://sharjeel45557.github.io/drug-app/feed.json")!

    private let cacheFilename = "feed-cache.json"
    private let session: URLSession

    init(session: URLSession = .shared) {
        self.session = session
    }

    // MARK: Lifecycle

    /// Call once on launch: load whatever we have locally, then refresh.
    func bootstrap() async {
        loadLocal()
        await refresh()
    }

    /// Pull-to-refresh / manual refresh entry point.
    func refresh() async {
        isLoading = true
        errorMessage = nil
        defer { isLoading = false }

        do {
            var request = URLRequest(url: feedURL)
            request.cachePolicy = .reloadIgnoringLocalCacheData
            request.timeoutInterval = 20
            let (data, response) = try await session.data(for: request)

            guard let http = response as? HTTPURLResponse, (200..<300).contains(http.statusCode) else {
                throw FeedError.badStatus
            }

            let feed = try JSONDecoder().decode(Feed.self, from: data)
            apply(feed)
            saveCache(data)          // persist newest for offline next launch
        } catch {
            // Keep showing whatever is on screen; surface a gentle message.
            if articles.isEmpty {
                errorMessage = "Couldn't load the latest feed. Showing bundled stories."
            } else {
                errorMessage = "Showing the last saved feed — pull to retry."
            }
        }
    }

    // MARK: Local sources

    /// Prefer the on-disk cache; fall back to the seed bundled in the app.
    private func loadLocal() {
        if let url = cacheURL, let data = try? Data(contentsOf: url),
           let feed = try? JSONDecoder().decode(Feed.self, from: data) {
            apply(feed)
            return
        }
        if let url = Bundle.main.url(forResource: "seed-feed", withExtension: "json"),
           let data = try? Data(contentsOf: url),
           let feed = try? JSONDecoder().decode(Feed.self, from: data) {
            apply(feed)
        }
    }

    private func apply(_ feed: Feed) {
        // Newest first; the pipeline already numbers ids 1…N top-down.
        articles = feed.articles.sorted {
            ($0.publishedDate ?? .distantPast) > ($1.publishedDate ?? .distantPast)
        }
        weekRange = feed.weekRange
        lastUpdated = feed.generatedDate
    }

    // MARK: Disk cache

    private var cacheURL: URL? {
        let dir = FileManager.default.urls(for: .cachesDirectory, in: .userDomainMask).first
        return dir?.appendingPathComponent(cacheFilename)
    }

    private func saveCache(_ data: Data) {
        guard let url = cacheURL else { return }
        try? data.write(to: url, options: .atomic)
    }

    enum FeedError: Error { case badStatus }
}
