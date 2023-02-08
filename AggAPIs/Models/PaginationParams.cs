namespace AggAPIs.Models
{
    public class PaginationParams
    {
        private int _maxElementsPerPage = 50;
        public int itemsPerPage;
        public int Page { get; set; } = 1;
        public int ItemsPerPage
        {
            get => itemsPerPage;
            set => itemsPerPage = value > _maxElementsPerPage ? _maxElementsPerPage : value;
        }
    }
}
