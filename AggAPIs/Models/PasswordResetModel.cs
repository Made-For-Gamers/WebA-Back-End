namespace AggAPIs.Models
{
    public class PasswordResetModel
    {
        public string Hash { get; set; }
        public string Email{get; set;}
        public string NewPassword{get; set;}
    }
}
