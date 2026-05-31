import SwiftUI

@main
struct PharmaPulseApp: App {
    @StateObject private var store = FeedStore()

    var body: some Scene {
        WindowGroup {
            FeedView()
                .environmentObject(store)
                .tint(Theme.accent)
                .task { await store.bootstrap() }
        }
    }
}
